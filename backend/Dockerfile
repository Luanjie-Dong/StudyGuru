# Use an official JDK runtime as a parent image
FROM eclipse-temurin:21-jdk

# Set the working directory inside the container
WORKDIR /

# Copy the built JAR file into the container
COPY target/backend-0.0.1-SNAPSHOT.jar backend-0.0.1-SNAPSHOT.jar

# Copy the .env file to the working directory
COPY src/main/resources/.env .env

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "backend-0.0.1-SNAPSHOT.jar"]
