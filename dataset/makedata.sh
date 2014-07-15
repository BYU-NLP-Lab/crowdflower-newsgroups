#!/bin/sh
echo "removing old json files from tmp"
rm -r tmp
mkdir tmp

# turn crowdflower annotations into an annotation stream
echo "translating crowdflower data into an annotation stream"
/usr/bin/python3 ~/git/utils/annotation_streams/crowdflower/convert.py -b /aml/data/newsgroups -o tmp/annotated.json ../results/1000/untrusted/job_505945.json 

# translate crowdflower annotations from period-delimited to underscore delimited
echo "translating all dots to underscores in crowdflower annotations"
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py alt.atheism alt_atheism tmp/annotated.json > tmp/01.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py comp.graphics comp_graphics tmp/01.json > tmp/02.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py comp.os.ms-windows.misc comp_os_ms-windows_misc tmp/02.json > tmp/03.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py comp.sys.ibm.pc.hardware comp_sys_ibm_pc_hardware tmp/03.json > tmp/04.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py comp.sys.mac.hardware comp_sys_mac_hardware tmp/04.json > tmp/05.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py comp.windows.x comp_windows_x tmp/05.json > tmp/06.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py misc.forsale misc_forsale tmp/06.json > tmp/07.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py rec.autos rec_autos tmp/07.json > tmp/08.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py rec.motorcycles rec_motorcycles tmp/08.json > tmp/09.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py rec.sport.baseball rec_sport_baseball tmp/09.json > tmp/10.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py rec.sport.hockey rec_sport_hockey tmp/10.json > tmp/11.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py sci.crypt sci_crypt tmp/11.json > tmp/12.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py sci.electronics sci_electronics tmp/12.json > tmp/13.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py sci.med sci_med tmp/13.json > tmp/14.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py sci.space sci_space tmp/14.json > tmp/15.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py soc.religion.christian soc_religion_christian tmp/15.json > tmp/16.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py talk.politics.guns talk_politics_guns tmp/16.json > tmp/17.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py talk.politics.mideast talk_politics_mideast tmp/17.json > tmp/18.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py talk.politics.misc talk_politics_misc tmp/18.json > tmp/19.json
/usr/bin/python3 ~/git/utils/annotation_streams/translate.py talk.religion.misc talk_religion_misc tmp/19.json > tmp/20.json

# turn unannotated data into an "annotation" stream
echo "translating excluded data into an annotation stream"
/usr/bin/python3 unannotatedcsv2json.py -b /aml/data/newsgroups -o tmp/unannotated.json ../input/excluded.csv

# combine the two streams into the full annotation stream dataset
echo "combining annotated and unannotated data into a single annotation stream"
/usr/bin/python3 ~/git/utils/annotation_streams/append.py tmp/20.json tmp/unannotated.json > cfgroups1000.json

