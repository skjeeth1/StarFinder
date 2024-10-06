WINDOW_HEIGHT = 640
WINDOW_LENGTH = 1280

TITLE_FONT = "assets/fonts/sterion-font/Sterion-BLLld.ttf"
FONT = "assets/fonts/audiowide-font/Audiowide-Regular.ttf"

PLANET_DATA = {
    (360, 273): ("Dips in Light", "Exoplanet HAT-P-7b",
                 "HAT-P-7b (or Kepler-2b) is an extrasolar planet discovered in 2008. It orbits very close to its host star and is larger and more massive than Jupiter.",
                 "Discovery: Transit", "Planet Type: Gas Giant", "Year: 2008"),
    (382, 295): ("Dips in Light", 'Exoplanet Kepler-1625b',
                 "Kepler-1625b is a super-Jupiter exoplanet orbiting the Sun-like star Kepler-1625 about 2,500 parsecs (8,200 light-years) away in the constellation of Cygnus.",
                 "Discovery: Transit", "Planet Type: Neptune-like", "Year: 2016"),
    (371, 420): ("Reading the Wobble", "Exoplanet HD-209458b",
                 "HD 209458 b is an exoplanet that orbits the solar analog HD 209458 in the constellation Pegasus, some 157 light-years from the Solar System.",
                 "Discovery: Radial Velocity", "Planet Type: Gas Giant", "Year: 1999"),
    (1018, 107): ("Dips in Light", "Exoplanet K2-18b",
                  "K2-18b, also known as EPIC 201912552 b, is an exoplanet orbiting the red dwarf K2-18, located 124 light-years away from Earth. Initially discovered with the Kepler space telescope, it was later observed by the James Webb Space Telescope in order to study the planet's atmosphere.",
                  "Discovery: Transit", "Planet Type: Super Earth", "Year: 2015"),
    (396, 517): ("Dips in Light", "Exoplanet TRAPPIST-1e",
                 "TRAPPIST-1e, is a rocky, close-to-Earth-sized exoplanet orbiting within the habitable zone around the ultracool dwarf star TRAPPIST-1, located 40.7 light-years away from Earth in the constellation of Aquarius.",
                 "Discovery: Transit", "Planet Type: Super Earth", "Year: 2016"),
    (861, 333): (
    "Reading the Wobble", "Exoplanet HD-189733b", "", "Discovery: Radial Velocity", "Planet Type: Gas Giant",
    "Year: 2005"),
}

FINDER_DATA = {
    "Reading the Wobble": ("Aka: Radial Velocity",
                           "This method involves making precise measurements of a star's position to detect the tiny wobble caused by an orbiting planet."),
    "Dips in Light": ("AKA: Transit",
                      "When a planet passes in front of its star, it blocks some of the star's light, which creates a small decrease in the observed light. The depth of the decrease is proportional to the planet's cross-section"),
    "Reading the Light": ("AKA: Transit Spectroscopy",
                          "It's a technique known as 'transit spectroscopy,' when light from a star travels through the atmosphere of an orbiting planet and reaches our telescopes – in space or on the ground – and tells about where it's been."),
    "Direct Imaging": ("",
                       "This method captures pictures of exoplanets orbiting distant stars. It's very difficult to do, but it provides scientists with a lot of data about the planet, including its orbit and atmosphere.")
}

GAME_LORE = [
    [
        "Commander: Let's recap your mission one more time.",
        "Commander: Our AI is stolen because of those stupid multi-headed aliens.",
        "Commander: We need you sergeant to use this old piece of tech to find those multi-headed freaks' planet",
        "Commander: before they reach, and take back our precious AI before they do something with her ;(",
        "Commander: But how did our grandparents find these planets?     .    .    .",
        "Narrator: Find exoplanets in the night sky using the map. ",
        "Narrator: You can use Stellarium-web.org or the NASA website to get information.",
        "Commander: LOOK!!! They're trying to steal something from us. They are invisible in our radar.",
        "Commander: Fly the F/A 18 Hornet sergeant. This is going to get out of control.",
        "Narrator: Goto the mini game tab and shoot the enemies down."
    ],
    [
        "Commander: You did good sergeant bringing down those aliens! Too bad none survived.",
        "Commander: Hmmm.. Looks likes this information is good! These aliens did us good by stealing some of ",
        "Commander: these old encyclopedias.",
        "Narrator: Goto the Exoplanet Finder page in the menu tab (top-left). Read about the information provided",
        "Narrator: You can also view information about found exoplanets in the almanac tab of the menu.",
        "Surroundings: BANGGGGGG!!!",
        "Commander: OVER THERE!!!! Looks like these are the last ones! Try to keep them alive sergeant, ",
        "Commander: and keep yourself dust free!",
        "Narrator: Goto the mini game tab and fend off the last wave of aliens."
    ],
    [
        "Commander: Looks like they are going back to their base, huh?",
        "Commander: Habitable planets, hmmm? Didn't hear a lot about them from my grandparents.",
        "Narrator: May be the almanac contains information about the planets you might've missed.",
    ],
    [
        "Narrator: The planet you've choose is correct.",
        "Commander: Yay! You have saved the world, sergeant!",
        "Commander: The AI is safe and sound because of you!",
    ],
    [
        "Commander: NOOOOOO!!!! They have escaped with vital information about earth!",
        "Commander: Now we have no more information about where they escaped to!",
    ]
]
