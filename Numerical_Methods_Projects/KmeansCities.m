% Load the dataset
filePath = 'C:/Users/Diablo/Desktop/worldcities.csv';
data = readtable(filePath);

% Extract relevant features (Latitude, Longitude, Population)
latitude = data.lat;
longitude = data.lng;
population = data.population;

% Combine latitude, longitude, and population into a single matrix
geo_features = [latitude, longitude, population];

% Remove rows with missing data (applies to all features)
geo_features = rmmissing(geo_features);

% Split back into individual features after removing missing data
latitude = geo_features(:,1);
longitude = geo_features(:,2);
population = geo_features(:,3);

% Handle any zero or negative population values
valid_indices = population > 0; % Only keep rows where population > 0
latitude = latitude(valid_indices);
longitude = longitude(valid_indices);
population = population(valid_indices);

% Normalize the latitude and longitude
[normalized_features, mu, sigma] = normalize([latitude, longitude]); % Only normalize lat/lon

% Scale population for marker size
scaled_population = (population / max(population)) * 400 + 5; % Ensure all marker sizes > 0

% Apply K-means clustering
k = 4; % Number of clusters
[idx, C] = kmeans(normalized_features, k);

% Denormalize centroids for plotting
denormalized_C = C .* sigma + mu;

% Visualize the clusters in 2D with population represented by marker size
figure;
scatter(latitude, longitude, scaled_population, idx, 'filled'); % Plot cities with population size
hold on;
scatter(denormalized_C(:,1), denormalized_C(:,2), 100, 'kx', 'LineWidth', 2); % Plot centroids
title('K-means Clustering of Cities (2D with Population)');
xlabel('Latitude');
ylabel('Longitude');
legend('Cities (size ~ population)', 'Centroids');
grid on;

% Applying Elbow Rule to find the optimum number of clusters
k_values = 1:10;    % Test k from 1 to 10
ssd = zeros(size(k_values)); % Creating a vector to store the SSDs

for i = 1:length(k_values)
    k = k_values(i);
    [~, ~, sumd] = kmeans(normalized_features, k); % kmeans returns sum of distances (sumd)
    ssd(i) = sum(sumd); % Store total SSD for this k
end

% Plotting the Elbow Curve
figure;
plot(k_values, ssd, '-o', 'LineWidth', 2);
title('Elbow Method for Optimal k');
xlabel('Number of Clusters (k)');
ylabel('Sum of Squared Distances (SSD)');
grid on;

% --------------------------- K-medoids Clustering -----------------------------

% Apply K-medoids clustering
k_medoid_k = 4;
[idx_kmedoids, C_kmedoids] = kmedoids(normalized_features, k_medoid_k);

% Denormalize medoid positions for plotting
denormalized_C_kmedoids = C_kmedoids .* sigma + mu;

% Visualize the clusters in 2D with population represented by marker size (K-medoids)
figure;
scatter(latitude, longitude, scaled_population, idx_kmedoids, 'filled'); % Plot cities with population size
hold on;
scatter(denormalized_C_kmedoids(:,1), denormalized_C_kmedoids(:,2), 100, 'kx', 'LineWidth', 2); % Plot medoids
title('K-medoids Clustering of Cities (2D with Population)');
xlabel('Latitude');
ylabel('Longitude');
legend('Cities (size ~ population)', 'Medoids');
grid on;
