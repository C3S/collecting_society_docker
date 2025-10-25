Audioneex Test
==============

Links
-----

- https://www.audioneex.com/
- https://audioneex.readthedocs.io/en/latest/index.html
- https://github.com/a-gram/audioneex

Usage
-----

Note: For other examples and all parameters see top comments in `example#.c` files.

1. Build docker image::

    docker compose build audioneex

2. Create database folder::

    mkdir -p volumes/audioneex/database

3. Prepare some audio files::

    cd volumes/audioneex
    wget 'https://archive.org/compress/C3SIX__The_C3S_Ignition_Mix-14588/formats=OGG%20VORBIS&file=/C3SIX__The_C3S_Ignition_Mix-14588.zip'
    unzip C3SIX__The_C3S_Ignition_Mix-14588.zip -d C3SIgnitionMix

4. Start container and change into example folder::

    docker compose run --rm audioneex bash
    > cd /shared/audioneex-1.3.2/_build/linux-x64-gnu1420/release

5. Fingerprint and index files::

    > ./example1 -u /data/database /data/C3SIgnitionMix
    [FID:1] - LXDU_-_21_-_Into_The_Void.ogg ... OK. (00:06:55) (ID3)
    [FID:2] - Dr_Freebs_-_13_-_Blocks.ogg ... OK. (00:06:22) (ID3)
    [FID:3] - Strobotone_-_12_-_San_Fran_Interlude_Edit.ogg ... OK. (00:06:40) (ID3)
    [FID:4] - Die_Leere_im_Kern_Deiner_Hoffnung_-_07_-_Es_ist_nie_genug.ogg ... OK. (00:04:00) (ID3)
    [FID:5] - Marco_Trovatello_-_08_-_Bracers_Of_Chaos.ogg ... OK. (00:05:38) (ID3)
    [FID:6] - Strobotone_-_15_-_Surpreme_Theme.ogg ... OK. (00:03:59) (ID3)
    [FID:7] - Dr_Freebs_-_02_-_Sunshine.ogg ... OK. (00:03:37) (ID3)
    [FID:8] - Wolf_Nilson_Trio_-_04_-_Auf_der_anderen_Seite.ogg ... OK. (00:06:03) (ID3)
    [FID:9] - Ingvo_-_05_-_Verdichtung.ogg ... OK. (00:04:36) (ID3)
    [FID:10] - Klabauter_-_17_-_Plattenspiel.ogg ... OK. (00:02:46) (ID3)
    [FID:11] - Eric_Eckhart_plus_Salonband_-_03_-_The_One.ogg ... OK. (00:03:27) (ID3)
    [FID:12] - Singvgel_-_09_-_Pegasus.ogg ... OK. (00:05:59) (ID3)
    [FID:13] - Marco_Trovatello_-_14_-_Be_Sweet.ogg ... OK. (00:03:27) (ID3)
    [FID:14] - Sudio_-_16_-_Circuit_Bent.ogg ... OK. (00:07:41) (ID3)
    [FID:15] - Von_Korf_-_10_-_Marktversagen.ogg ... OK. (00:05:38) (ID3)
    [FID:16] - pandorasbox_-_22_-_Arrows__Bows.ogg ... OK. (00:04:50) (ID3)
    [FID:17] - angstalt_-_01_-_fr_eine_hand_voll_zucker_a-g_lang_mix_4.ogg ... OK. (00:08:30) (ID3)
    [FID:18] - Raziel_Jamaerah_-_11_-_The_Ooze_feat_Bruder_Johanna_Ferdinand_Tschecker_and_PlizBis.ogg ... OK. (00:05:44) (ID3)
    [FID:19] - epilog_-_19_-_Morgen_danach_prod_by_locoto.ogg ... OK. (00:05:29) (ID3)
    [FID:20] - ZOELEELA_-_20_-_IAMARMX.ogg ... OK. (00:04:04) (ID3)
    [FID:21] - Marco_Trovatello_-_18_-_A_Turn.ogg ... OK. (00:06:15) (ID3)
    Flushing...
    Done

6. Match fingerprints from audio::

    > ./example3 -u /data/database /data/C3SIgnitionMix
    Identifying LXDU_-_21_-_Into_The_Void.ogg ...
    =========================================================
    IDENTIFIED  FID: 1
    Score: 30408.3, Conf.: 0.994802, Id.Time: 4.8s
    Into The Void by LXDU
    =========================================================
    ID Time: 4.8 s
    Identifying Dr_Freebs_-_13_-_Blocks.ogg ...
    =========================================================
    IDENTIFIED  FID: 2
    Score: 20813.7, Conf.: 0.992083, Id.Time: 4.8s
    Blocks by Dr Freebs
    =========================================================
    ID Time: 4.8 s
    Identifying Strobotone_-_12_-_San_Fran_Interlude_Edit.ogg ...
    =========================================================
    IDENTIFIED  FID: 3
    Score: 28510.5, Conf.: 0.99744, Id.Time: 6s
    San Fran Interlude (Edit) by Strobotone
    =========================================================
    ID Time: 6 s
    Identifying Die_Leere_im_Kern_Deiner_Hoffnung_-_07_-_Es_ist_nie_genug.ogg ...
    =========================================================
    IDENTIFIED  FID: 4
    Score: 33606.4, Conf.: 0.997626, Id.Time: 3.6s
    Es ist nie genug by Die Leere im Kern Deiner Hoffnung
    =========================================================
    ID Time: 3.6 s
    Identifying Marco_Trovatello_-_08_-_Bracers_Of_Chaos.ogg ...
    =========================================================
    IDENTIFIED  FID: 5
    Score: 29587.3, Conf.: 0.998982, Id.Time: 4.8s
    Bracers Of Chaos by Marco Trovatello
    =========================================================
    ID Time: 4.8 s
    Identifying Strobotone_-_15_-_Surpreme_Theme.ogg ...
    =========================================================
    IDENTIFIED  FID: 6
    Score: 45448.6, Conf.: 0.995804, Id.Time: 3.6s
    Surpreme Theme by Strobotone
    =========================================================
    ID Time: 3.6 s
    Identifying Dr_Freebs_-_02_-_Sunshine.ogg ...
    =========================================================
    IDENTIFIED  FID: 7
    Score: 26771.9, Conf.: 0.994802, Id.Time: 4.8s
    Sunshine by Dr Freebs
    =========================================================
    ID Time: 4.8 s
    Identifying Wolf_Nilson_Trio_-_04_-_Auf_der_anderen_Seite.ogg ...
    =========================================================
    IDENTIFIED  FID: 8
    Score: 58395.3, Conf.: 0.99647, Id.Time: 6s
    Auf der anderen Seite by Wolf Nilson Trio
    =========================================================
    ID Time: 6 s
    Identifying Ingvo_-_05_-_Verdichtung.ogg ...
    =========================================================
    IDENTIFIED  FID: 9
    Score: 26857.7, Conf.: 0.994653, Id.Time: 4.8s
    Verdichtung by Ingvo
    =========================================================
    ID Time: 4.8 s
    Identifying Klabauter_-_17_-_Plattenspiel.ogg ...
    =========================================================
    IDENTIFIED  FID: 10
    Score: 32416.8, Conf.: 0.996885, Id.Time: 4.8s
    Plattenspiel by Klabauter
    =========================================================
    ID Time: 4.8 s
    Identifying Eric_Eckhart_plus_Salonband_-_03_-_The_One.ogg ...
    =========================================================
    IDENTIFIED  FID: 11
    Score: 47977.2, Conf.: 0.995927, Id.Time: 4.8s
    The One by Eric Eckhart plus Salonband
    =========================================================
    ID Time: 4.8 s
    Identifying Singvgel_-_09_-_Pegasus.ogg ...
    =========================================================
    IDENTIFIED  FID: 12
    Score: 38339.7, Conf.: 0.997531, Id.Time: 4.8s
    Pegasus by Singvgel
    =========================================================
    ID Time: 4.8 s
    Identifying Marco_Trovatello_-_14_-_Be_Sweet.ogg ...
    =========================================================
    IDENTIFIED  FID: 13
    Score: 10928, Conf.: 0.997898, Id.Time: 6s
    Be Sweet by Marco Trovatello
    =========================================================
    ID Time: 6 s
    Identifying Sudio_-_16_-_Circuit_Bent.ogg ...
    =========================================================
    IDENTIFIED  FID: 14
    Score: 23569.5, Conf.: 0.995453, Id.Time: 6s
    Circuit Bent by Sudio
    =========================================================
    ID Time: 6 s
    Identifying Von_Korf_-_10_-_Marktversagen.ogg ...
    =========================================================
    IDENTIFIED  FID: 15
    Score: 40593.4, Conf.: 0.997748, Id.Time: 4.8s
    Marktversagen by Von Korf
    =========================================================
    ID Time: 4.8 s
    Identifying pandorasbox_-_22_-_Arrows__Bows.ogg ...
    =========================================================
    IDENTIFIED  FID: 16
    Score: 36980, Conf.: 0.998813, Id.Time: 3.6s
    Arrows and Bows by pandoras.box
    =========================================================
    ID Time: 3.6 s
    Identifying angstalt_-_01_-_fr_eine_hand_voll_zucker_a-g_lang_mix_4.ogg ...
    =========================================================
    IDENTIFIED  FID: 17
    Score: 16794.8, Conf.: 0.994791, Id.Time: 6s
    fr eine hand voll zucker (a.-g. lang mix #4) by /'angstalt/
    =========================================================
    ID Time: 6 s
    Identifying Raziel_Jamaerah_-_11_-_The_Ooze_feat_Bruder_Johanna_Ferdinand_Tschecker_and_PlizBis.ogg ...
    =========================================================
    IDENTIFIED  FID: 18
    Score: 43361.2, Conf.: 0.998358, Id.Time: 6s
    The Ooze (feat. Bruder, Johanna, Ferdinand Tschecker and PlizBis) by Raziel Jamaerah
    =========================================================
    ID Time: 6 s
    Identifying epilog_-_19_-_Morgen_danach_prod_by_locoto.ogg ...
    =========================================================
    IDENTIFIED  FID: 19
    Score: 14146.4, Conf.: 0.995386, Id.Time: 4.8s
    Morgen danach (prod. by locoto) by epilog
    =========================================================
    ID Time: 4.8 s
    Identifying ZOELEELA_-_20_-_IAMARMX.ogg ...
    =========================================================
    IDENTIFIED  FID: 20
    Score: 22760.2, Conf.: 0.991387, Id.Time: 4.8s
    IAMARMX by ZOE.LEELA
    =========================================================
    ID Time: 4.8 s
    Identifying Marco_Trovatello_-_18_-_A_Turn.ogg ...
    =========================================================
    IDENTIFIED  FID: 21
    Score: 30981.5, Conf.: 0.992108, Id.Time: 3.6s
    A Turn by Marco Trovatello
    =========================================================
    ID Time: 3.6 s
    Done

