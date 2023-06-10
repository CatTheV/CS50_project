from project import clean, nick_only, remove_stopwords


def main():
    test_clean()
    test_nick_only()
    test_remove_stopwords()


def test_clean():
    assert clean("RT @journoturk: Hope continues 6 days after the #earthquake in #Turkey.") == "Hope continues 6 days after the earthquake in Turkey"
    assert clean("RT @Lerpc75: 🇹🇷#Earthquake in #Turkey") == "Earthquake in Turkey"
    assert clean("RT @DailyLoud: Anonymous donor gives stunning $30 Million toward Turkey/Syria earthquake victims 🙏 https://t.co/cfvi1M9818") == "Anonymous donor gives stunning 30 Million toward TurkeySyria earthquake victims"


def test_nick_only():
    assert nick_only("RT @journoturk: Hope continues 6 days after the #earthquake in #Turkey.") == "@journoturk"
    assert nick_only("RT @bora_twts: [Official] Kmedia reports HYBE has donated ₩500M ($412k) to the international children’s NGO Save the Children to aid in the…") == "@bora_twts"
    assert nick_only("Turkey detains building contractors as death toll rises to 33,000 : NPR https://t.co/MLvidKDag3") == None

def test_remove_stopwords():
    assert remove_stopwords("The school requested not to come to school on the test day") == "school requested not come school test day"
    assert remove_stopwords("Not, no") == "Not , no"
    assert remove_stopwords("A to the on an upon") == "upon"


if __name__ == "__main__":
    main()