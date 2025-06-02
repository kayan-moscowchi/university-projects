% Load the dataset
data = readtable('heart.csv'); % Adjust file name/path as needed

% Preprocess the dataset
% Convert categorical columns to numeric
data.Sex = grp2idx(data.Sex); % Convert 'Sex' (M/F) to numeric
data.ChestPainType = grp2idx(data.ChestPainType); % Convert 'ChestPainType'
data.RestingECG = grp2idx(data.RestingECG); % Convert 'RestingECG'
data.ExerciseAngina = grp2idx(data.ExerciseAngina); % Convert 'ExerciseAngina'
data.ST_Slope = grp2idx(data.ST_Slope); % Convert 'ST_Slope'

% Normalize numeric columns
numericCols = {'Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak'};
for i = 1:numel(numericCols)
    col = numericCols{i};
    data.(col) = (data.(col) - min(data.(col))) / (max(data.(col)) - min(data.(col)));
end

% Extract the target variable
heartDisease = data.HeartDisease; % Extract the HeartDisease column
data = table2array(data(:, 1:end-1)); % Exclude HeartDisease from feature set

% Parameters
k = 2; % Number of clusters (assuming 2 groups: heart disease vs. no heart disease)
maxIter = 100; % Maximum number of iterations

% Initialize medoids
n = size(data, 1);
medoids = randperm(n, k); % Random initialization

% Variables
clusters = zeros(n, 1);
prev_medoids = zeros(1, k);
iter = 0;

% K-medoids algorithm
while ~isequal(medoids, prev_medoids) && iter < maxIter
    iter = iter + 1;
    prev_medoids = medoids;

    % Assigning points to the nearest medoid
    for i = 1:n
        distances = zeros(1, k);
        for j = 1:k
            distances(j) = sum((data(i, :) - data(medoids(j), :)).^2);
        end
        [~, clusters(i)] = min(distances);
    end

    % Updating medoids based on distances
    for j = 1:k
        clusterPoints = find(clusters == j);

        % Compute total distances for all points in the cluster
        totalDistances = zeros(length(clusterPoints), 1);
        for p = 1:length(clusterPoints)
            pointIdx = clusterPoints(p);
            % Computing local distance matrix and outputting the row wise sum
            totalDistances(p) = sum(sum((data(clusterPoints, :) - data(pointIdx, :)).^2, 2));
        end

        % Update medoid to minimize total distance
        [~, minIdx] = min(totalDistances);
        medoids(j) = clusterPoints(minIdx);
    end
end

% Output results
fprintf('Algorithm converged in %d iterations.', iter);
disp('Final Medoids Indices:');
disp(medoids);


% Visualize clusters and compare with HeartDisease
% Implementing Principal component analysis to visualize 2D
coeff = pca(data); 
data2D = data * coeff(:, 1:2); % Reduce to 2D

% Create scatter plot for clustering results
figure;
subplot(1, 2, 1); % Divides the figure into a 1-row, 2-column grid focuses on first
hold on;
colors = lines(k); % Use distinct colors for clusters which are predefined
for i = 1:k
    scatter(data2D(clusters == i, 1), data2D(clusters == i, 2), 50, colors(i, :), 'filled');
end
scatter(data2D(medoids, 1), data2D(medoids, 2), 100, 'k', 'x', 'LineWidth', 2); % Marking medoids
title('K-Medoids Clustering Results');
xlabel('Principal Component 1');
ylabel('Principal Component 2');

% Defining cluster and medoid labels using anonymous function 
clusterLabels = arrayfun(@(x) sprintf('Cluster %d', x), 1:k, 'UniformOutput', false);
legend([clusterLabels, {'Medoids'}], 'Location', 'best');
hold off;

% Create scatter plot for actual HeartDisease labels
subplot(1, 2, 2); % Second plot: Ground truth
hold on;
scatter(data2D(heartDisease == 0, 1), data2D(heartDisease == 0, 2), 50, 'b', 'filled');
scatter(data2D(heartDisease == 1, 1), data2D(heartDisease == 1, 2), 50, 'r', 'filled');
title('Actual HeartDisease Distribution');
xlabel('Principal Component 1');
ylabel('Principal Component 2');
legend({'No Heart Disease', 'Heart Disease'}, 'Location', 'best');
hold off;

% Initialize an array to store mapped cluster labels
mappedClusters = zeros(size(clusters));

% Iterate through each unique cluster
for clusterIdx = unique(clusters)'
    % Find the indices of data points in this cluster
    clusterPoints = (clusters == clusterIdx);
    
    % Find the true HeartDisease labels for these points
    clusterHeartDisease = heartDisease(clusterPoints);
    
    % Assign the most common HeartDisease label to the entire cluster
    mappedClusters(clusterPoints) = mode(clusterHeartDisease);
end

% Calculate the clustering accuracy
correctAssignments = sum(mappedClusters == heartDisease);
accuracy = correctAssignments / numel(heartDisease);

% Display the accuracy
fprintf('Clustering Accuracy: %.2f%%\n', accuracy * 100);