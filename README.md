# Github Java Insight
1. Quickstart
see dockerfile

2. Introduction
Our goal this hackathon was to visualize a developer's Java abilities based on their publically available GitHub profile. There are already many publically available tools for analyzing GitHub profiles, so we wanted to create a product that would both provide comparable functionality while also introducing some novel insights. Ultimately, our goal was to have a website that help hiring managers or recruiters evaluate potential candidates.

We identified five areas of interest for scoring Java developers:
* versatility
* code quality
* community engagement
* best practices
* GitHub activity

Our app computes these metrics and aggregates them to assign a final score. It also displays a breakdown of all the individual results that contributed to these metrics.
Our project is unique in that it sources information not only from GitHub metadata, but it also performs an analysis of the code itself. Additionally, we added a feature to compare the compatibility of two engineers based on their metric subscores.

3. Tech Stack
Our front-end is built on Vue.js and our backend uses Flask (Python). We use a combination of PyGitHub (v3 API calls) and GraphQL (v4 API calls for dependency graph). Our code quality analysis uses `google-java-format`. We provide a Dockerfile to automate the build and deployment process.

4. Scoring
    * GitHub Activity - This metric contains some basic information about how active a user is on GitHub, particularly with respect to forks, stars, and issues on their repositories.
    * Versatility - GitHub computes a dependency graph for each repository that scans for files used by Maven (among other package managers). We use the API to determine which packages are most used by a given developer across all their repositories. A user's versatility score is a function of the frequencies of their top 10 used packages.
    * Best Practices - We check for multiple characteristics of a good developer - whether they include descriptive README files, whether they use branches to manage versions, and whether they have Maven or Gradle files in their repositories.
    * Code Quality - In order to evaluate the quality of a user's Java code, we run the `google-java-format` package on all their Java repositories and compute which fraction of their code violates the style guidelines.
    * Community - This metric measures how engaged a developer is with the open source community. This includes features such as whether their comments contribute to closing open issues on other repositories, and how long it takes them to respond to and resolve their own issues.

5. Comparison
One common criteria for hiring an engineer is determining how compatible they are with the other engineers on the team or company that they are joining. We provide some insight into this by taking the cosine similarity of the metrics for two given engineers. This can be used to identify developers who prioritize similar factors, for example if a company really values code quality but doesn't care about open source engagement.
