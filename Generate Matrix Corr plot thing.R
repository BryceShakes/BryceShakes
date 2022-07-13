
library(tidyverse)
library(stringr)
library(scales)
library(ggthemes)

set.seed(5318008)

Ai_results <- read.csv("C:/Users/Bryce/OneDrive - University of Bristol/Documents/Intro to AI/AI project/group-project-10/Ai va Ai - rounds - results.csv")

target <- c('random','30000 rounds','60000 rounds','99999 rounds','300000 rounds','600000 rounds','999999 rounds')

test <- Ai_results[,2:4] %>% 
  rename(First_Player = First.Player, Second_Player = Second.Player, Results = Winner) %>% 
  group_by(First_Player, Second_Player) %>% 
  summarise(first_win_perc = (sum(ifelse(Results ==1, 1, 0))/n())*100,
            second_win_perc = (sum(ifelse(Results ==-1, 1, 0))/n())*100) %>% 
  arrange(factor(First_Player, levels = target),factor(Second_Player, levels = target))

test$First_Player <- gsub('_',' ',test$First_Player)
test$Second_Player <- gsub('_',' ',test$Second_Player)

beauty <- ggplot(test, aes(x = Second_Player, y = First_Player)) + 
  geom_tile(aes(fill = first_win_perc)) +
  theme_few() +
  scale_fill_gradient(low="white", high="red") +
  geom_text(aes(label = round(first_win_perc, 2), size = 10)) + 
  scale_x_discrete(limits=target) +
  scale_y_discrete(limits=target) +
  xlab('Second Player') + ylab('First Player')+
  labs(fill = 'Win %', title = 'AI vs AI - First Player Win Percentage') + 
  theme(plot.title = element_text(hjust = 0.5),  
        axis.text.y = element_text(angle=45, vjust = 0.5),
        axis.text.x = element_text(angle=45, hjust = 1, vjust = 1.1))



beauty

beauty2 <- ggplot(test, aes(x = Second_Player, y = First_Player)) + 
  geom_tile(aes(fill = second_win_perc)) + 
  theme_few() +
  scale_fill_gradient(low="white", high="purple") +
  geom_text(aes(label = round(second_win_perc, 2))) + 
  scale_x_discrete(limits=target) +
  scale_y_discrete(limits=target) +
  xlab('Second Player') + ylab('First Player') +
  labs(fill = 'Win %', title = 'AI vs AI - Second Player Win Percentage') + 
  theme(plot.title = element_text(hjust = 0.5),  
        axis.text.y = element_text(angle=45, vjust = 0.5),
        axis.text.x = element_text(angle=45, hjust = 1, vjust = 1.1))

beauty2

Size <- read.csv("C:/Users/Bryce/OneDrive - University of Bristol/Documents/Intro to AI/AI project/group-project-10/Size by rounds.csv")[2:7,2:3]

Size$Rounds <- as.numeric(gsub("([0-9]+).*$", "\\1", Size$Rounds))

beauty3 <- ggplot(Size, aes(x = Rounds, y = State_size)) +geom_bar(stat="identity", colour='deepskyblue', fill='deepskyblue') +
  geom_line(aes(y=(State_size / Rounds)*400000))+
  geom_point(aes(x=Rounds, y=(State_size / Rounds)*400000))+
  theme_few() +
  xlab('Rounds Ran to train')+
  ggtitle('Rounds and States comparison')+
  scale_y_continuous(name = "States Valued (Bar)", 
                     labels = comma,
                     sec.axis = sec_axis(~./400000, name="Average States Valued Per Round (Line)"))+
  theme(plot.title = element_text(hjust = 0.5), axis.text.y = element_text(angle=90, hjust = 0.5))

beauty3
#  scale_fill_continuous(limits=c(0, 1), breaks=seq(0,1,by=0.25))
