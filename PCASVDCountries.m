% Load and preprocess the dataset
% Load the dataset from the CSV file
filePath = 'C:/Users/Diablo/Desktop/Country-data.csv';
data = readtable(filePath); % Replace with the correct filename

% Check the first few rows of the data
disp('Preview of data:');
disp(head(data));

% Extract country names (assuming the first column contains names)
country_names = data{:, 1}; % First column is assumed to contain country names

% Extract numerical data (assuming the rest are numerical features)
X = table2array(data(:, 2:end)); 

% Handle missing or non-numeric data
% Check for missing values (NaN) and remove rows with missing values
if any(isnan(X), 'all')
    warning('Dataset contains NaN values. Removing rows with NaNs...');
    valid_rows = ~any(isnan(X), 2);
    country_names = country_names(valid_rows); % Keep only valid country names
    X = X(valid_rows, :); % Keep only valid rows of numerical data
end

% Standardize the data
% Subtract the mean and divide by standard deviation (feature scaling)
X_mean = mean(X, 1); % Mean of each column
X_std = std(X, 0, 1); % Standard deviation of each column
X_standardized = (X - X_mean) ./ X_std;

% Perform Singular Value Decomposition (SVD)
[U, D, V] = svd(X_standardized, 'econ'); % Perform thin SVD

% Compute the principal components (scores)
Z = U * D; % Z is now the projection of the data onto principal components

% Visualize countries projected onto PC1 and PC2
% Scatter plot of the first two principal components
figure;
scatter(Z(:, 1), Z(:, 2), 50, 'filled'); % Plot PC1 vs. PC2
hold on;

% Add labels to the points (ensure indices match)
for i = 1:length(country_names)
    text(Z(i, 1), Z(i, 2), country_names{i}, 'FontSize', 8, 'HorizontalAlignment', 'left');
end

xlabel('Principal Component 1');
ylabel('Principal Component 2');
title('Projection of Countries onto PC1 and PC2');
grid on;
hold off;

% Explained Variance
% Calculate variance explained by each principal component
singular_values = diag(D); % Extract singular values
explained_variance = (singular_values .^ 2) / sum(singular_values .^ 2) * 100;

% Display explained variance
disp('Explained variance by each principal component (%):');
disp(explained_variance);

% Scree Plot
figure;
plot(1:length(explained_variance), explained_variance, '-o');
xlabel('Principal Component');
ylabel('Explained Variance (%)');
title('Scree Plot: Explained Variance by Principal Components');
grid on;