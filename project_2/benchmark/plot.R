library("tidyverse")
data <- read_csv("benchmark.tsv")
data$algo <- as.factor(data$algo)
data |>
  ggplot(aes(x = length, y = user, color = algo))+
  geom_point()+
  geom_smooth()+
  facet_wrap(~algo) +
  xlab("Sequences length in nucletides")+
  ylab("User time in seconds")+
  theme_light()+
  theme(legend.position =  "None")+
  scale_color_manual(values = c("#cb6a49", "#a46cb7", "#7aa457")) -> p1

ggsave(p1, "benchmark.pdf", dpi = "print")

    