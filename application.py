import os
from flask import *
from src.game import BlackJack


application = Flask(__name__, template_folder='./templates/')
application.static_folder = './static'
application.secret_key = os.urandom(24)
PATH_DECK = "./static/deck/"
games = {}
keys = []
status = 0


def cards_to_html(cards, turn, hide):

    images_row = ""
    text_row = ""
    for card in cards:

        url = "{0}{1}.png".format(card[0], card[1].name)

        if card[0] == "Diamonds" or card[0] == "Hearts":
            color = "red"
        else:
            color = "black"

        # &diams; &spades; &hearts; &clubs; are the html symbols for the suits
        if card[0] == "Diamonds":
            text = "{0}<font color={1}>&{2};</font>".format(card[1].name, color, "diams")
        else:
            text = "{0}<font color={1}>&{2};</font>".format(card[1].name, color, card[0].lower())

        if turn == "player":

            images_row += "<td><center><img src=\"{0}\"/></center></td>".format(PATH_DECK + url)
            text_row += "<td><center><font color=\"{1}\">{0}</font></center></td>".format(text, color)

        elif turn == "dealer" and (hide == 3 or hide ==2 or hide ==4 or hide ==5):

            images_row += "<td><center><img src=\"{0}\"/ height = \"50\" width = \"40\" ></center></td>".format(PATH_DECK + url)
            text_row += "<td><center><font color=\"{1}\">{0}</font></center></td>".format(text, color)
        else:
            images_row = "<td><center><img src=\"{0}\"/ height = \"50\" width = \"40\" ></center></td>".format(PATH_DECK + url)
            text_row = "<td><center><font color=\"{1}\">{0}</font></center></td>".format(text, color)
            break

    if (hide == 1 or hide ==0) and turn == "dealer":
        images_row+= "<td><center><img src=\"{0}\"/ height = \"50\" width = \"40\" ></center></td>".format(PATH_DECK + 'card_hide.png')
        text_row+= "<td><center><font>{0}</font></center></td>".format("FaceDown")

    table = "<center><table><tr>{0}</tr><tr>{1}</tr></table></center>".format(images_row, text_row)
    return Markup(table)


def format_feed(all_feeds):
    feed = ""

    for f in all_feeds:
        if status == 3:
            feed += Markup("<p style='color:#22B70D';>") + f + Markup("</p>")
        elif status == 2 or status == 4:
            feed += Markup("<p style='color:#AB1515';>") + f + Markup("</p>")
        elif status == 5:
            feed += Markup("<p style='color:#EE9308';>") + f + Markup("</p>")
        else:
            feed += Markup("<p>") + f + Markup("</p>")

    if status == 2 or status == 3 or status == 4 or status == 5:
        feed += Markup("<p>") + "Press Reset to Play Again!" + Markup("</p>")

    return feed


@application.route("/")
def homepage():
    try:
        key = session['key']
        curr_game = games[key]
    except KeyError:
        return redirect(url_for("new_session"))

    feed = curr_game.get_feed(status)
    feed = format_feed(feed)
    # score = "{0} - {1}".format(G.player_wins, G.dealer_wins)

    return render_template("index.html", feed=feed,
                           player_hand=cards_to_html(curr_game.get_player_hand(), "player", status),
                           dealer_hand=cards_to_html(curr_game.get_dealer_hand(), "dealer", status), status=status)


@application.route("/__new_session")
def new_session():
    global status
    key = os.urandom(12)
    session['key'] = key
    games[key] = BlackJack()
    keys.append(key)
    games[key].start_game()
    status = 0

    if len(keys) >= 100:
        key = keys.pop(0)
        games.pop(key)

    return redirect(url_for("homepage"))


@application.route("/__hit")
def hit():
    global status
    try:
        key = session['key']
        curr_game = games[key]
    except KeyError:
        return redirect(url_for("new_session"))

    try:
        if status == 1 or status==0:
            status = curr_game.hit()
            flash(Markup("You drew a card."))
    except:
        flash(Markup("ERROR!!"))

    # return redirect(url_for("check"))
    return redirect(url_for("homepage"))


@application.route("/__reset")
def reset():
    return redirect(url_for("new_session"))


@application.route("/__stand")
def stand():
    global status
    try:
        key = session['key']
        curr_game = games[key]
    except KeyError:
        return redirect(url_for("new_session"))

    try:
        if status == 1 or status==0:
            status = curr_game.stand()
            flash(Markup("You decided to stand."))
    except:
        flash(Markup("ERROR!!"))

    # return redirect(url_for("check"))
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    application.run()
