% Loading the Iris dataset
load fisheriris;
data = meas;          % Features: Sepal and Petal measurements
labels = species;     % Class labels: Setosa, Versicolor, Virginica

% Display the first few rows with headers for better readability
disp('First 5 rows of the Iris Dataset:');
disp('----------------------------------');
disp(' SepalLength  SepalWidth  PetalLength  PetalWidth');
disp(head(data));

% Encode class labels as numeric
classLabels = grp2idx(labels); % Convert class names to numeric: 1, 2, 3

% Compute the overall mean of the data
overallMean = mean(data);

% Compute class means and within-class scatter matrix (Sw)
uniqueClasses = unique(classLabels);  % Unique class identifiers
numClasses = numel(uniqueClasses);    % Number of classes
numFeatures = size(data, 2);          % Number of features
Sw = zeros(numFeatures, numFeatures); % Initialize within-class scatter matrix

% Loop over each class to compute Sw
for i = 1:numClasses
    % Extract data for the current class
    classData = data(classLabels == uniqueClasses(i), :);
    
    % Compute the mean of the current class
    classMean = mean(classData);
    
    % Compute the scatter matrix for the class and add to Sw
    classScatter = (classData - classMean)' * (classData - classMean);
    Sw = Sw + classScatter;
end

% Compute the between-class scatter matrix (Sb)
Sb = zeros(numFeatures, numFeatures); % Initialize between-class scatter matrix

% Loop over each class
for i = 1:numClasses
    % Extract data for the current class
    classData = data(classLabels == uniqueClasses(i), :);
    
    % Compute the mean of the current class
    classMean = mean(classData);
    
    % Compute the number of samples in the class
    classSize = size(classData, 1);
    
    % Compute the scatter contribution for the class and add to Sb
    meanDifference = (classMean - overallMean)';
    Sb = Sb + classSize * (meanDifference * meanDifference');
end

% Solve the generalized eigenvalue problem for Sw^-1 * Sb
[eigenVectors, eigenValues] = eig(Sw \ Sb);

% Sort eigenvalues and eigenvectors in descending order
[~, sortIdx] = sort(diag(eigenValues), 'descend');
eigenVectors = eigenVectors(:, sortIdx);

% Project data onto the first (numClasses - 1) LDA components
% For Iris dataset, numClasses = 3, so numClasses - 1 = 2
ldaComponents = eigenVectors(:, 1:numClasses-1);
ldaTransformedData = data * ldaComponents;

% Visualize the results
gscatter(ldaTransformedData(:,1), ldaTransformedData(:,2), labels);
xlabel('LD1');
ylabel('LD2');
title('LDA Projection of Iris Dataset');
