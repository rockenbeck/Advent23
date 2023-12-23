# 37.806549, -88.982817
# 30.406610, -90.861646
# 38.105424, -86.943245
# 64.755369, -147.353578

# print(37-88+30-90+38-86+64-147)


# 697 Sleepy Hollow Rd, Briarcliff Manor, NY 10510
# Pedro Bay, AK 99647
# 209 Old Connecticut Path, Wayland, MA 01778
# Charlotte Amalie, St Thomas 00802, USVI
# 4968 Willowstone Dr, Highland, UT 84003
# 572 S 300 W, Springville, UT 84663
# Hayneville, AL 36040
# 2475 Tongass Ave, Ketchikan, AK 99901
# 213 Table Mountain Blvd, Oroville, CA 95965
# 11272 Rustic Rd, Rough and Ready, CA 95975
# 21 Stovepipe Corner Rd, Castle Hill, ME 04757

# Briarcliff Manor, Pedro Bay, Wayland, Charlotte Amalie, Highland, Springville, Hayneville, Ketchikan, Oroville, Rough and Ready, Castle Hill



s="""38002	Arlington	Shelby County
38002	Lakeland	Shelby County
38014	Brunswick	Shelby County
38016	Cordova	Shelby County
38017	Fisherville	Shelby County
38017	Collierville	Shelby County
38018	Cordova	Shelby County
38027	Collierville	Shelby County
38028	Eads	Shelby County
38029	Ellendale	Shelby County
38053	Millington	Shelby County
38054	Millington	Shelby County
38083	Millington	Shelby County
38088	Cordova	Shelby County
38101	Memphis	Shelby County
38103	Memphis	Shelby County
38104	Memphis	Shelby County
38105	Memphis	Shelby County
38106	Memphis	Shelby County
38107	Memphis	Shelby County
38108	Memphis	Shelby County
38109	Memphis	Shelby County
38111	Memphis	Shelby County
38112	Memphis	Shelby County
38113	Memphis	Shelby County
38114	Memphis	Shelby County
38115	Hickory Hill	Shelby County
38115	Memphis	Shelby County
38116	Memphis	Shelby County
38117	Memphis	Shelby County
38118	Memphis	Shelby County
38119	Memphis	Shelby County
38120	Memphis	Shelby County
38122	Memphis	Shelby County
38124	Memphis	Shelby County
38125	Hickory Hill	Shelby County
38125	Memphis	Shelby County
38126	Memphis	Shelby County
38127	Memphis	Shelby County
38128	Memphis	Shelby County
38130	Memphis	Shelby County
38131	Memphis	Shelby County
38132	Memphis	Shelby County
38133	Bartlett	Shelby County
38133	Memphis	Shelby County
38134	Bartlett	Shelby County
38134	Memphis	Shelby County
38135	Bartlett	Shelby County
38135	Memphis	Shelby County
38137	Memphis	Shelby County
38138	Germantown	Shelby County
38138	Memphis	Shelby County
38139	Germantown	Shelby County
38139	Memphis	Shelby County
38141	Memphis	Shelby County
38157	Memphis	Shelby County
38167	Memphis	Shelby County
38168	Memphis	Shelby County
38173	Memphis	Shelby County
38174	Memphis	Shelby County
38175	Memphis	Shelby County
38177	Memphis	Shelby County
38181	Memphis	Shelby County
38182	Memphis	Shelby County
38183	Germantown	Shelby County
38184	Memphis	Shelby County
38186	Memphis	Shelby County
38187	Memphis	Shelby County
38190	Memphis	Shelby County"""

total = 0
for line in s.split('\n'):
    zip,city = line.split('\t')[0:2]
    if city == "Memphis":
        print(zip, city)
        total += int(zip)
print(f"total = {total}")