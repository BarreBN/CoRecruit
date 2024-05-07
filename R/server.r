library(shiny)
library(ggplot2)
library(dplyr)

# Server logic
server <- function(input, output) {
  data <- reactive({
    # Read the CSV file
    jobs <- read.csv("job_data.csv", stringsAsFactors = FALSE)
    if (input$city != "All") {
      jobs <- jobs[jobs$workplace_address_city == input$city, ]
    }
    jobs
  })
  
  output$plotJobFields <- renderPlot({
    req(data())
    jobData <- data()
    # Assuming there's a job field column named 'employment_type_label' in your CSV
    topFields <- jobData %>%
      count(employment_type_label, sort = TRUE) %>%
      top_n(10)
    ggplot(topFields, aes(x = reorder(employment_type_label, n), y = n)) +
      geom_bar(stat = "identity", fill = "steelblue") +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      labs(title = "Most Common Job Fields", x = "Field", y = "Number of Jobs")
  })
  
  output$plotTopJobs <- renderPlot({
    req(data())
    jobData <- data()
    # Assuming 'description_text' column contains job titles or similar descriptions
    topJobs <- jobData %>%
      count(description_text, sort = TRUE) %>%
      top_n(10)
    ggplot(topJobs, aes(x = reorder(description_text, n), y = n)) +
      geom_bar(stat = "identity", fill = "coral") +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      labs(title = "Top Jobs", x = "Job", y = "Number of Jobs")
  })
  
  output$plotNonDrivingJobs <- renderPlot({
    req(data())
    jobData <- data()
    # Filtering jobs where 'driving_license_required' is 'No'
    ndJobs <- jobData %>% 
      filter(driving_license_required == "No")
    topNDJobs <- ndJobs %>%
      count(description_text, sort = TRUE) %>%
      top_n(10)
    ggplot(topNDJobs, aes(x = reorder(description_text, n), y = n)) +
      geom_bar(stat = "identity", fill = "green") +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      labs(title = "Top Jobs without Driver's License Requirement", x = "Job", y = "Number of Jobs")
  })
}
