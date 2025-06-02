% Load sonar dataset
filename = 'C:/Users/Diablo/Desktop/sonar data.csv';
data = readtable(filename);

% Convert the table to an array for processing
X = table2array(data(:, 1:end-1));  % Feature matrix (exclude last column)
Y = data{:, end};  % Target labels (Mines or Rocks)

% Convert categorical labels ('M' for Mine, 'R' for Rock) to numeric values
Y_numeric = strcmp(Y, 'M');  % Mines = 1 (true), Rocks = 0 (false)

% Parameters for NMF
num_components = 7;  % Number of components (k)
max_iter = 500;      % Maximum number of iterations
tolerance = 1e-3;    % Convergence tolerance

% Initialize W and H randomly with non-negative values
rng(42);  % Set seed for reproducibility
[m, n] = size(X);
W = abs(rand(m, num_components));  % Non-negative m x k matrix
H = abs(rand(num_components, n));  % Non-negative k x n matrix

% Perform NMF using iterative multiplicative update rules
for iter = 1:max_iter
    W_prev = W;  % Store previous W
    H_prev = H;  % Store previous H
    
    % Update H (holding W fixed)
    H = H .* ((W' * X) ./ (W' * W * H + eps)); %eps to prevent division by zero 
    
    % Update W (holding H fixed)
    W = W .* ((X * H') ./ (W * H * H' + eps));
    
    % Compute convergence based on sum of differences
    delta_W = sum(abs(W - W_prev), 'all');  % Change in W
    delta_H = sum(abs(H - H_prev), 'all');  % Change in H
    total_change = delta_W + delta_H;       % Total change

    % Check for convergence
    if total_change < tolerance
        fprintf('Converged after %d iterations with total change %.6f\n', iter, total_change);
        break;
    end
end

if iter == max_iter
    fprintf('Reached max iterations (%d) with final total change %.6f\n', max_iter, total_change);
end

% Split data into training and testing sets (80% train, 20% test)
cv = cvpartition(size(W,1), 'HoldOut', 0.2);
X_train = W(training(cv), :);
Y_train = Y_numeric(training(cv));

X_test = W(test(cv), :);
Y_test = Y_numeric(test(cv));

% Train a linear discriminant analysis classifier
model = fitcdiscr(X_train, Y_train);

% Predict on test data
Y_pred = predict(model, X_test);

% Evaluate the classification performance
accuracy = sum(Y_pred == Y_test) / length(Y_test);
fprintf('Classification Accuracy: %.2f%%\n', accuracy * 100);

% Confusion matrix (Contingency Table)
confusionchart(Y_test, Y_pred);
title('Confusion Matrix of Sonar Data Classification');

% Visualize the NMF Features
figure;
scatter(W(Y_numeric == 1, 1), W(Y_numeric == 1, 2), 'r', 'DisplayName', 'Mines');
hold on;
scatter(W(Y_numeric == 0, 1), W(Y_numeric == 0, 2), 'b', 'DisplayName', 'Rocks');
xlabel('Component 1');
ylabel('Component 2');
title('NMF Features for Sonar Data');
legend;
grid on;
hold off;
