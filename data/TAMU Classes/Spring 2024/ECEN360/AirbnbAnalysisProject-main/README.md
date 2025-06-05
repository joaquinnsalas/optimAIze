---

# Airbnb Analysis Project

This repository contains all the necessary materials for running the Airbnb Analysis Project, including a Jupyter notebook, data files, and a Dockerfile. The environment is packaged into a Docker container to ensure reproducibility and ease of use.

## Getting Started

### Prerequisites

Before you can run this project, you must have Docker installed on your computer. If you do not have Docker installed, please download and install it from [Docker's official website](https://www.docker.com/get-started/).

### Installation

1. **Download the Repository**

    Click on the green "Code" button at the top of this GitHub repository, and download the ZIP file of the code. Extract the contents to a convenient location on your computer.

2. **Build the Docker Image**

    Open a terminal and navigate to the directory where you extracted the project files. Run the following command to build the Docker image:

    ```bash
    docker build -t airbnbanalysis:0.0.1 .
    ```

    This command builds a Docker image named `airbnbanalysis` with the tag `0.0.1` using the Dockerfile in the current directory.

3. **Run the Docker Container**

    After the image has been built, run the container using the following command:

    ```bash
    docker run -v /YourPath/AirbnbAnalysisProject:/home/notebooks -p 8888:8888 --name Analysis airbnbanalysis:0.0.1
    ```

    Replace `/path/to/your/AirbnbAnalysisProject` with the absolute path to the `AirbnbAnalysisProject` folder on your computer. This command mounts the specified directory into the container and forwards port 8888 to access the Jupyter notebook.

   If when you run the container and click on the link and it shows up blank, change the formatting of your file path.
   
    ```bash
   //c/Users/YourUsername/Downloads/AirbnbAnalysisProject:/home/notebooks -p 8888:8888 --name Analysis airbnbanalysis:0.0.1
    ```
    
### Accessing the Jupyter Notebook

After running the Docker container, you will see an output in the terminal that includes a URL starting with `http://127.0.0.1:8888/` followed by a token. Copy this URL and paste it into your web browser to access the Jupyter notebook.

## Repository Contents

- **Dockerfile**: Contains all the commands to assemble the Docker image.
- **notebook**: Jupyter notebook with the analysis.
- **data**: Data files used in the notebooks.
- **Contribution Report**: A report of how each team member contributed to this project.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
