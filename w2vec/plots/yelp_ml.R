
## install.packages('ggplot2')
library(ggplot2)  


setwd('/Users/jshankar/Dropbox/yelp_ml/')
df <- read.csv('finaldata.csv')
nr <- nrow(df)

df$no_of_words                <- as.integer(df$no_of_words)
df$no_of_reviews              <- as.integer(df$no_of_reviews)
df$unique_no_of_food_entities <- as.integer(df$unique_no_of_food_entities)
df$no_of_food_entities        <- as.integer(df$no_of_food_entities)
df$avg_rating                 <- as.numeric(df$avg_rating)

## group the restuarants with rating 
df$rating = rep(NA, nr)
for (i in 1:nr) {
  if (df$avg_rating[i] < 3) {
    df$rating[i] <- "BAD"
  } else if (df$avg_rating[i] < 4 ) {
    df$rating[i] <- "OK"
  } else {
    df$rating[i] <- "GOOD"
  }
}
df$rating <- as.factor(df$rating)
print (summary(df))

##avg_rating
ggplot(data=df, aes(x=avg_rating)) + geom_histogram(aes(fill=rating))
ggsave('avg-rating.png')

## no_of_reviews
ggplot(data=df, aes(x=no_of_reviews)) + geom_density(aes(fill=rating), alpha=0.3)
ggsave('no-of-reviews.png')

## no_of_words
ggplot(data=df, aes(x=no_of_words)) + geom_density(aes(fill=rating), alpha=0.3)
ggsave('no-of-words.png')

# unique_no_of_food_entities
ggplot(data=df, aes(x=unique_no_of_food_entities)) + geom_histogram(aes(fill=rating))
ggsave('unique-no-of-food-entities.png')

# no_of_words vs unique_no_of_food_entities
ggplot(data=df, aes(x=no_of_words, y = unique_no_of_food_entities)) + geom_point(aes(color=rating), shape=1) + facet_grid(rating ~ .) 
ggsave('no-of-words-vs-unique-no-of-food-entities.png')

# no_of_reviews vs unique_no_of_food_entities
ggplot(data=df, aes(x=no_of_reviews, y = unique_no_of_food_entities)) + geom_point(aes(color=rating), shape=1) + facet_grid(rating ~ .) 
ggsave('no-of-reviews-vs-unique-no-of-food-entities.png')


