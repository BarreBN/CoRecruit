library(shiny)
library(jsonlite)
library(DT)

# Define UI
ui <- fluidPage(
  titlePanel("View JSONL Data"),
  DTOutput("dataTable")
)

# Define server logic
server <- function(input, output) {
  output$dataTable <- renderDT({
    # Initialize an empty list to store each line's data
    dataList <- list()
    
    # Read the .jsonl file line by line
    # Replace the path with the actual path to your .jsonl file
    con <- file("FILE_PATH", "r")
    while (TRUE) {
      line <- readLines(con, warn = FALSE, n = 1)
      if (length(line) == 0) {
        break
      }
      dataList[[length(dataList) + 1]] <- fromJSON(line)
    }
    close(con)
    
    # Combine all data into a single dataframe
    dataTable <- do.call(rbind, lapply(dataList, as.data.frame))
    
    # Use DT::datatable() for interactive table display
    DT::datatable(dataTable, options = list(pageLength = 10))
  })
}

# Run the application
shinyApp(ui = ui, server = server)
