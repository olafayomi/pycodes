# Script Name : rock_scissor_paper.py
# Author : Dimeji Fayomi
# Created : 2015/05/27
# Version : 1.0
# Description : A rock, scissor, paper game to be played betweeen human and  computer player,
#               the human choses an option and the computer choice one option at random and a winner
#               is determined.

import random
from sys import exit

human_score = 0
computer_score = 0

# keep the score of the game, true for human wins and false for computer
def score_keeper(bool_winner):
    global human_score
    global computer_score
    if bool_winner == True:
       human_score += 1
    else:
       computer_score += 1
    print "Your Score is:", human_score
    print "Computer's score is:", computer_score
    print "\n"
# Function that controls the game
def play_logic(rounds):
    comp_list = ['rock','scissors','paper']
    while rounds != 0 :
        print """
            Please press:
            'a' to choose rock,
            'b' to choose scissors,
            'c' to choose paper.
            """
        human = raw_input("Enter your choice:")
        computer = random.choice(comp_list)
        
        print "Computer chose: ",computer
         
        if human == 'a' and computer == 'rock':
           print "We have a draw"
        elif human == 'a' and computer == 'scissors':
           print "Rock crushes scissors, Human wins!!!"
           score_keeper(True)
        elif human == 'a' and computer == 'paper':
           print "Paper covers rock, Computer wins!!!"
           score_keeper(False)
        elif human == 'b' and computer == 'rock':
           print "Rock crushes scissors, Computer wins!!!"
           score_keeper(False)
        elif human == 'b' and computer == 'scissors':
           print "We have a draw"
        elif human == 'b' and computer == 'paper':
           print "Scissors cuts paper, Human wins!!!"
           score_keeper(True)
        elif human == 'c' and computer == 'rock':
           print "Paper covers rock, Humans wins!!!"
           score_keeper(True)
        elif human == 'c' and computer == 'scissors':
           print "Scissors cuts paper, Computer wins!!!"
           score_keeper(False)
        elif human == 'c' and computer == 'paper':
           print "We have a draw"  
        else:
           print "No sensible option chosen"
  
        rounds -= 1
        
def decide_winner(human_score,computer_score):
    if human_score > computer_score:
        print "Human wins the set"
    elif human_score < computer_score:
        print "Computer wins the set"
    else:
        print "We have a draw, Too bad!!!"

print "Welcome to the Rock, Scissor, Paper game"
print "You will be playing against the computer"

# Get the number of rounds to be played in each game
num_of_rounds = int(raw_input("Please enter the number of rounds:"))

if num_of_rounds >= 0:
    play_logic(num_of_rounds)
    decide_winner(human_score,computer_score)
else:
    print "Number must be greater than zero!!!"
    exit(0)

   
