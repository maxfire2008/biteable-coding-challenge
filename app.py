from flask import Flask
from pprint import pprint
import os
import csv
app = Flask(__name__)

def import_file(text):
    output = []
    headers = None
    reader = csv.reader(text.splitlines(), delimiter=",", quotechar="|")
    for row in reader:
##        print(row)
        if headers == None:
            headers = row
        else:
            try:
                output.append([
                        row[headers.index("ID")],
                        row[headers.index("ITEM")],
                        row[headers.index("PARENT")]
                            ])
            except Exception as e:
##                print(e,"on row",row)
                None
    return output

def get_children(parent,data):
    children = []
##    print(data)
    for item in data:
##        print(item,item[2]==parent)
        if item[2] == parent:
            children.append({item[0]:get_children(item[0],data)})
    return children

def get_item(data,n):
    for current_item in data:
        if current_item[0] == n:
            break
    return current_item

def format_children(data,children,indent_length=0):
    lines = []
    for child in children:
##        print(get_item(data,list(child)[0])[1])
##        print(child[list(child)[0]])
##        print(format_children(data,child[list(child)[0]]),indent_length+1)
##        lines+=[" "*(indent_length*2)+"+ "+get_item(data,list(child)[0])[1]]
        if child[list(child)[0]] != []:
            lines+=['<li><span class="caret">'+get_item(data,list(child)[0])[1]+'</span><ul class="nested">']
            lines+=format_children(data,child[list(child)[0]],indent_length+1)
            lines+=['</ul></li>']
        else:
            lines+=['<li style="margin-left:4vw;">'+get_item(data,list(child)[0])[1]+'</li>']
    return lines
##    print(current_item[1])

def get_lines(text):
    data = import_file(text)
    children = get_children("nil",data)
    lines=format_children(data,children)
##    print(repr(lines))
    return '\n'.join(lines)


##if __name__ == "__main__":
##    print(get_lines(open("input2.txt").read()))

@app.route("/")
def index():
    file_content = open(os.environ.get("LISTFILE","input2.txt")).read()
    return '<!DOCTYPE html><head><title>Biteable Coding Challenge</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body>'+'<ul id="myUL">'+get_lines(file_content)+'''</ul><style>/* Remove default bullets */
ul, #myUL {
  list-style-type: none;
}

/* Remove margins and padding from the parent ul */
#myUL {
  margin: 0;
  padding: 0;
}

/* Style the caret/arrow */
.caret {
  cursor: pointer;
  user-select: none; /* Prevent text selection */
}

/* Create the caret/arrow with a unicode, and style it */
.caret::before {
  content: "\\25B6";
  color: #fcba03;
  display: inline-block;
  margin-right: 3vw;
}

/* Rotate the caret/arrow icon when clicked on (using JavaScript) */
.caret-down::before {
  transform: rotate(90deg);
}

/* Hide the nested list */
.nested {
  display: none;
}

/* Show the nested list when the user clicks on the caret/arrow (with JavaScript) */
.active {
  display: block;
}
* {
  font-size: 3vmin;
  font-family: sans-serif;
}
</style>
<script>
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}
</script></body>'''
