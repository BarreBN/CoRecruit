library(shiny)

ui <- fluidPage(
  titlePanel("Job Market Analysis"),
  sidebarLayout(
    sidebarPanel(
      selectInput("city", "Choose a City:", choices = c("All")),
      actionButton("update", "Update Views")
    ),
    mainPanel(
      tabsetPanel(type = "tabs",
                  tabPanel("Job Fields", plotOutput("plotJobFields")),
                  tabPanel("Top Jobs", plotOutput("plotTopJobs")),
                  tabPanel("Non-Driving Jobs", plotOutput("plotNonDrivingJobs"))
      )
    )
  )
)
