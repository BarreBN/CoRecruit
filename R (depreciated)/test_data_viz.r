library(shiny)
library(jsonlite)
library(ggplot2)
library(dplyr)

# Define UI
ui <- fluidPage(
  titlePanel("Number of Jobs in Different Categories"),
  plotOutput("jobCategoryPlot")
)

# Define server logic
server <- function(input, output) {
  data <- reactive({
    # Load and preprocess job data from the JSON file
    # Replace with the correct path to your JSON file
    jsonData <- fromJSON("C:/Users/bthur/Downloads/subset_data.json", flatten = TRUE)
    
    # Extract the occupation.label column, assuming it contains the job category
    # Use dplyr to handle data cleaning and preparation
    jobData <- as.data.frame(jsonData) %>%
      select(occupation.label) %>%
      filter(!is.na(occupation.label))
    
    return(jobData)
  })
  
  output$jobCategoryPlot <- renderPlot({
    jobData <- data()
    
    # Count the number of jobs in each category
    categoryCounts <- jobData %>%
      group_by(occupation.label) %>%
      summarise(Count = n())
    
    # Plot the counts using ggplot2
    ggplot(categoryCounts, aes(x = occupation.label, y = Count)) +
      geom_bar(stat = "identity") +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      labs(x = "Job Category", y = "Number of Jobs", title = "Jobs per Category")
  })
}

# Run the application
shinyApp(ui = ui, server = server)
