import pygame
import random
import sys

pygame.init()

# Configurări generale
WIDTH, HEIGHT = 800, 600
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('arial', 24)

# Simboluri pentru cărți
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
          '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def hand_value(hand):
    value = sum(values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def draw_text(surface, text, x, y, color=WHITE):
    label = FONT.render(text, True, color)
    surface.blit(label, (x, y))

def draw_hand(surface, hand, x, y):
    for i, card in enumerate(hand):
        rank, suit = card
        card_text = f"{rank}{suit}"
        pygame.draw.rect(surface, WHITE, (x + i*70, y, 60, 90))
        draw_text(surface, card_text, x + i*70 + 10, y + 30, BLACK)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blackjack Game")
    clock = pygame.time.Clock()

    deck = create_deck()
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    game_over = False
    player_turn = True
    result = ""

    while True:
        screen.fill(GREEN)
        draw_text(screen, "Blackjack - PyGame Edition", 280, 20)
        draw_text(screen, "Your Hand:", 50, 120)
        draw_hand(screen, player_hand, 50, 150)

        draw_text(screen, "Dealer's Hand:", 50, 300)
        if game_over:
            draw_hand(screen, dealer_hand, 50, 330)
        else:
            draw_hand(screen, [("?", "?")] + dealer_hand[1:], 50, 330)

        if result:
            draw_text(screen, result, 280, 500)
            draw_text(screen, "Press R to restart", 280, 530)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

                if player_turn and not game_over:
                    if event.key == pygame.K_h:  # Hit
                        player_hand.append(deck.pop())
                        if hand_value(player_hand) > 21:
                            result = "You busted! Dealer wins 😭"
                            game_over = True
                            player_turn = False
                    elif event.key == pygame.K_s:  # Stand
                        player_turn = False

        if not player_turn and not game_over:
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            p_val = hand_value(player_hand)
            d_val = hand_value(dealer_hand)
            if d_val > 21 or p_val > d_val:
                result = "You win! 🤩"
            elif d_val == p_val:
                result = "Tie! 😑"
            else:
                result = "Dealer wins! 😭"
            game_over = True

        clock.tick(30)

if __name__ == '__main__':
    main()
