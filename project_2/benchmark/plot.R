library("tidyverse")
library(latex2exp)
data <- read_csv("benchmark.csv") |>
  separate(
    col = algo,into = c("backtrack", "algo"),sep = "backtrack_"
    )
data$algo <- as.factor(data$algo)
data$backtrack <- as.factor(data$backtrack)
levels(data$backtrack) <- c("With backtrack", "Without backtrack")
base_plot <- function(data, ...){
  data |>
    ggplot(aes(...))+
    geom_point(alpha = 0.7)+
    facet_wrap(~backtrack) +
    theme_light()+
    theme(legend.position =  "bottom")+
    scale_color_manual(values = c("#cb6a49", "#a46cb7", "#7aa457"))
}

# User time Vs sequence length 
(
  p1 <- base_plot(data, x = length, y = user, color = algo)+
    xlab(TeX(r"($N$)"))+
    ylab(TeX(r"($T)"))
  )
#ggsave(p1, filename = "user_time_vs_length.pdf", width = 210, height = 297, units = "mm")

# Log N vs Log T

(p2 <- base_plot(data, x = log(length), y = log(user), color = algo))
#ggsave(p1, filename = "log_user_time_vs_log_ength.pdf", width = 210, height = 297, units = "mm")

# Calculate base level

data |>
  filter(length == 0) |>
  group_by(algo, backtrack) |>
  summarise(
    mean = mean(user), sd = sd(user)
  )
# Let's take the average
base_level <- data |>
  filter(length == 0) |>
  pull(user)|>
  mean()

(
  p3 <- data |>
    filter(length > 0)|>
    mutate(user = user-base_level)|>
    base_plot(x = log(length), y = log(user), color = algo)+
    xlab(TeX(r"($\log(N)$)"))+
    ylab(TeX(r"($\log(T))"))
  )
#ggsave(p3, filename = "log_user_time_minus_base_vs_log_ength.pdf", width = 210, height = 297, units = "mm")


# N  vs T / n²
( p4 <- data|>
  filter(length > 0)|>
  mutate(user = user-base_level)|>
  base_plot(data, x = length, y = user/(length^2), color = algo)+
  xlab(TeX(r"($N$)"))+
  ylab(TeX(r"($\frac{T}{N^2}$)"))
  
 )
#ggsave(p4, filename = "user_time_corrected_divided_n_length_vs_length.pdf", width = 210, height = 297, units = "mm")

library(cowplot)

plot_grid(p1, p3, p4,nrow = 2,)
