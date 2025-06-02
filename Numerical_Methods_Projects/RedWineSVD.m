% Load the dataset from the CSV file
filePath = 'C:/Users/Diablo/Desktop/Red.csv'; % Path to the uploaded file
dataTable = readtable(filePath);

% Display the first few rows of the dataset
disp('Dataset Preview:');
disp(head(dataTable));

% Extract numerical columns for SVD
numericData = dataTable{:, {'Rating', 'NumberOfRatings', 'Price', 'Year'}};

% Check for missing values and handle them
% Replace NaN values with the column mean
for i = 1:size(numericData, 2)
    col = numericData(:, i);
    if any(isnan(col))
        colMean = mean(col, 'omitnan'); % Compute column mean ignoring NaN
        col(isnan(col)) = colMean; % Replace NaN with the mean
        numericData(:, i) = col;
    end
end

% Normalize the data (optional, for better scaling)
numericData = normalize(numericData);

% Display the numeric matrix
disp('Numeric Data for SVD:');
disp(head(numericData));

% Perform Singular Value Decomposition
[U, S, V] = svd(numericData);

% Display the results
disp('Left Singular Vectors (U):');
disp(U(1:5, 1:10));

disp('Singular Values (Diagonal Matrix S):');
disp(head(S));

disp('Right Singular Vectors (V):');
disp(head(V));

% Reconstruct the matrix using k singular values (Thin SVD)
k = 2; % Number of singular values to retain
Uk = U(:, 1:k);
Sk = S(1:k, 1:k);
Vk = V(:, 1:k);

reconstructedMatrix = Uk * Sk * Vk';

% Display the reconstructed matrix
disp('Reconstructed Matrix (Using Top k Singular Values):');
disp(head(reconstructedMatrix));

% Calculate reconstruction error
reconstructionError = norm(numericData - reconstructedMatrix, 'fro');
disp('Reconstruction Error When k = 2:');
disp(reconstructionError);

% Singular Values Visualization
singularValues = diag(S);
figure;
plot(singularValues, 'o-');
xlabel('Component Index');
ylabel('Magnitude of Singular Value');
title('Singular Values and Variance Contribution');
grid on;
