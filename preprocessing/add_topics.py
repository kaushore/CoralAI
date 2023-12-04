import pandas as pd
import unicodedata

def normalize_unicode(text):
    output = []
    for word in text.split(' '):
        try:
            meaning = unicodedata.name(word).lower()
            output.append(meaning)
        except TypeError:
            output.append(word)
    return " ".join(output)

with open("data.txt","r",encoding="utf-8") as f:
    contents = f.read()

content_list = contents.split("#############################")[1:]

pattern = "*****************************"
chapter_name = ""
data = []
for idx,content in enumerate(content_list):
    split_content = content.split(pattern)
    chapter_name = split_content[0]
    for c in split_content[1:]:
        if c != "\n\n\n":
            data_dict = {}
            data_dict["Chapter"] = chapter_name.split("_")[0].replace("\n"," ")
            data_dict["Page_number"] = chapter_name.split("_")[-1].replace("\n#######\n","")
            data_dict["Topic"] = c.split("@")[0].replace("\n"," ").strip()
            paragraph = chapter_name.split("_")[0].replace("\n"," ") + "@" + c.replace("\n"," ")
            data_dict["Paragraph"] = normalize_unicode(paragraph)
            data.append(data_dict)

# print(len(data))

for idx,d in enumerate(data):
    d["pid"] = idx

print(data[4])

csv_df = pd.DataFrame(data)

csv_df.to_csv("office-collections.csv",index=False)

df = pd.DataFrame(columns=["pid","passage"])
df["pid"] = csv_df["pid"]
df["passage"] = csv_df["Paragraph"]

tsv_file = 'collections.tsv'

# Write the DataFrame to a TSV file
df.to_csv(tsv_file, sep='\t', index=False)

# print(content_list[1].split("*****************************")[0].split("_")[0])