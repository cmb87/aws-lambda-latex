data = {
    "qr": {"generate": True, "data": "Hi I'm Chad"},
    "business": {
        "name": "byte87",
        "website": "https://byte87.net",
        "slogan": "PoCs. Made. Simple.",
        "owner": "Dr.-Ing. Christian Peeren",
        "email": "christian.peeren@gmail.com",
        "address": ["Krefelder Str.9", "47918 Toenisvorst", "Germany"],
        "includeBankDetails": False,
        "bank": {
            "name": "Sparkasse Krefeld",
            "iban": "DE49 3200 0000 0065 7539 17",
            "bic": "DESPKRDE33XX"
            },
    },
    "invoice": {
        "id": "1337",
        "dueDate": "August 20, 2020",
        "createDate": "August 10, 2020",
        "data": [
            {
                "VAT": "19.0",
                "id": "1",
                "name":"myawsomeproject",
                "products": [
                    {"type":"fee", "name": "Job1", "amount": "3", "cost": "3"},
                    {"type":"discount", "name": "Family and Friends", "cost": "23"},
                    {"type":"expense", "name": "Hotel", "cost": "323", "currency": "Dollar", "factor": "0.82"},
                ]
             },
            {
                "VAT": "19.0",
                "id": "2",
                "name": "myawsomeproject2",
                "products": [
                    {"type": "fee", "name": "Job1", "amount": "3", "cost": "3"},
                    {"type": "discount", "name": "Family and Friends", "cost": "23"},
                    {"type": "expense", "name": "Hotel", "cost": "323", "currency": "Dollar", "factor": "0.82"},
                ]
            }
        ]
    },
    "customer": {
        "id": "123",
        "shipTo": ["Yolo Gmbh", "Ser Olfe", "Fat Beats Str 123", "34192 Lol City", "Germany"],
        "billTo": ["Yolo Gmbh2", "Ser Olfe2", "Fat Beats Str 223", "34192 Lol City", "Germany"],
    }
}


def createInvoiceTemplate(filename, data):
    # ===================================
    templatePreamble=r"""\documentclass[a4paper]{letter}
    \usepackage{graphicx}% The demo option creates a black box instead of a figure
    \usepackage{fancyhdr}
    \usepackage{invoice} 
    \usepackage{blindtext}
    \usepackage{geometry}
    \usepackage{calc}
    \usepackage{color}
    \usepackage{xcolor}
    %\usepackage[T1]{fontenc}
    
    % https://texblog.org/2011/01/27/add-your-logo-to-the-title-page/
    % ---------------------------------------------------------------
    % Change default Font
    \renewcommand{\sfdefault}{qcr}
    \renewcommand{\familydefault}{\sfdefault}
    \longindentation=0pt % Signature left aligned
    
    % ---------------------------------------------------------------
    % Invoice new commads
    \renewcommand{\Fees}{Products}
    \renewcommand{\UnitRate}{Price}
    \renewcommand{\Count}{Quantity}
    \renewcommand{\Activity}{Product}
    % ---------------------------------------------------------------
    """

    # ===================================
    templateHeader="\n"
    templateHeader+="% ---------------------------------------------------------------\n"
    templateHeader+="% Your data\n"
    templateHeader+=r"\address{_}"+"\n"
    templateHeader+=r"\telephone{_}"+"\n"
    templateHeader+="% ---------------------------------------------------------------\n"
    templateHeader+="% Save standard definitions\n"
    templateHeader+="\let\HeadRule\headrule\n"
    templateHeader+="\let\FootRule\\footrule\n"
    templateHeader+="\n"

    for site in ["firstpage", "empty", "plain"]:
        templateHeader+=r"\fancypagestyle{"+site+r"}"+"{%\n"
        templateHeader+=r"    \renewcommand{\headrulewidth}{0.5pt}%"+"\n"
        templateHeader+=r"    \renewcommand{\footrulewidth}{0.5pt}%"+"\n"
        templateHeader+=r"    \renewcommand\headrule{\color{gray}\HeadRule} %\renewcommand{\footrule}{\hbox to\headwidth{\color{gray}\leaders\hrule height \footrulewidth\hfill}}"+"\n"
        templateHeader+=r"    \renewcommand\footrule{\textcolor{gray}{\FootRule}}%"+"\n"
        templateHeader+=r"    \fancyfootoffset{1 cm}%"+"\n"
        templateHeader+=r"    \fancyheadoffset{1 cm}%"+"\n"
        templateHeader+=r"    \fancyhf{}%"+"\n"
        templateHeader+=r"    %\fancyhead[L]{\colorbox{black}{\parbox[b][\headheight-\baselineskip]{\headwidth}{\vfil{}\color{white} a\\a \vfil}}}%"+"\n"
        templateHeader+=r"    \fancyhead[C]{\vfil\includegraphics[height=0.7in, keepaspectratio=true]{logow.png} \\"+data["business"]["slogan"]+r"\hspace*{1.5ex} \vfil }%"+"\n"
        if data["business"]["includeBankDetails"]:
            templateHeader += r"    \fancyfoot[C]{{\fontfamily{qcr}\selectfont\color{gray}" + data["business"][
                "owner"] + " - " + data["business"]["email"] + r"\\" + data["business"]["bank"]["name"] + " - IBAN: " + \
                              data["business"]["bank"]["iban"] + " - BIC: " + data["business"]["bank"][
                                  "bic"] + r" \\ " + ' '.join(
                data["business"]["address"]) + r"}}" + "\n"

        else:
            templateHeader += r"    \fancyfoot[C]{{\fontfamily{qcr}\selectfont\color{gray}" + data["business"][
                "owner"] + " - " + data["business"]["email"] + r" \\ " + ' '.join(
                data["business"]["address"]) + r"}}" + "\n"

        templateHeader+="}%\n"



    templateHeader+=r"\setlength{\fboxsep}{0pt}"+"\n"
    templateHeader+=r"\geometry{top = 5cm, headheight = 4cm}"+"\n"
    templateHeader+=r"\fancyhfoffset[L]{\oddsidemargin + \hoffset + 1in}"+"\n"
    templateHeader+=r"\fancyhfoffset[R]{\evensidemargin + \marginparwidth - \marginparsep}"+"\n"
    templateHeader+="% ---------------------------------------------------------------\n"
    templateHeader+="\n"
    templateHeader+="% Address next to recepient\n"
    templateHeader+="\makeatletter\n"
    templateHeader+=r"\renewcommand*{\opening}[1]{\ifx\@empty\fromaddress%"+"\n"
    templateHeader+=r"  \thispagestyle{firstpage}%"+"\n"
    templateHeader+=r"    {\raggedleft\@date\par}%"+"\n"
    templateHeader+=r"  \else% home address"+"\n"
    templateHeader+=r"   \thispagestyle{empty}%"+"\n"
    templateHeader+=r"   {%"+"\n"
    templateHeader+=r"    \begin{minipage}[c]{0.50\linewidth}"+"\n"
    templateHeader+=r"    \textbf{Bill to:}\\"+"\n"
    templateHeader+=r"\\".join(data["customer"]["billTo"])+r"\\[0.5em]%"+"\n"
    templateHeader+=r"    \textbf{Ship to:}\\[0.1em]%\n"+"\n"
    templateHeader+=r"\\".join(data["customer"]["shipTo"])+r"\\[0.5em]%"+"\n"
    templateHeader+=r"    \end{minipage}"+"\n"
    templateHeader+=r"    \begin{minipage}[c]{0.45\linewidth}"+"\n"
    templateHeader+=r"    \raggedleft\begin{tabular}{l@{}}\ignorespaces"+"\n"
    templateHeader+=r"    "+data["business"]["website"]+r"\\%"+"\n"
    templateHeader+=r"    Customer ID: "+data["customer"]["id"]+r"\\%"+"\n"
    templateHeader+=r"    Project  ID: " + ', '.join([d["id"] for d in data["invoice"]["data"]]) + r"\\%" + "\n"
    templateHeader+=r"    Invoice ID: " + data["invoice"]["id"] + r"\\%" + "\n"
    if data["qr"]["generate"]:
        templateHeader+=r"    \includegraphics[height=2.5cm, keepaspectratio=true]{qr.png}\\[0.2em]%"+"\n"
    templateHeader+="    Invoice date: "+data["invoice"]["createDate"]+r"\\"+"\n"
    templateHeader+="    Due date: "+data["invoice"]["dueDate"]+r"\\"+"\n"
    #templateHeader+=r"    \@date"+"\n"
    templateHeader+=r"    \end{tabular}"+"\n"
    templateHeader+=r"    \end{minipage}"+"\n"
    templateHeader+=r"    \par"+"\n"
    templateHeader+=r"}%"+"\n"
    templateHeader+=r"  \fi"+"\n"
    templateHeader+=r"  \vspace{2\parskip}%"+"\n"
    templateHeader+=r"  #1\par\nobreak}"+"\n"
    templateHeader+=r"\makeatother"+"\n"

    templateDocument=""
    templateDocument+=r"% ---------------------------------------------------------------"+"\n"
    templateDocument+=r"% Start the document"+"\n"
    templateDocument+=r"% ---------------------------------------------------------------"+"\n"
    templateDocument+=r"\pagestyle{plain}"+"\n"
    templateDocument+=r"\begin{document}%"+"\n"
    templateDocument+=r"    \begin{letter}{%"+"\n"
    templateDocument+=r"\\".join(data["customer"]["shipTo"])+"\n"
    templateDocument+=r"}%"+"\n"
    templateDocument+=r"%"+"\n"

    templateDocument+= r"\opening{{\large \bf INVOICE} \\[1.0cm] Dear \toname{},}\hfil\\%"+"\n"
    templateDocument+= r"thank you very much for your order: %"+"\n"


    for project in data["invoice"]["data"]:

        templateDocument+=r"\begin{invoice}{Euro}{"+project["VAT"]+"}"+"\n"
        templateDocument+=r"\ProjectTitle{"+project["id"]+" - "+project["name"]+"} "+"\n"

        for prod in project["products"]:

            if prod["type"] == "fee":
                templateDocument += r"\Fee{"+prod["name"]+"}{"+prod["cost"]+"}{"+prod["amount"]+"}%\n"
            elif prod["type"] == "expense":
                templateDocument += r"\EFC{" + prod["name"] +  "}{" +prod["currency"]+  "}{" + prod["cost"] + "}{" + prod["factor"] + "}{}%\n"
            elif prod["type"] == "discount":
                templateDocument += r"\Discount{" + prod["name"] + "}{" + prod["cost"] + "}%\n"

        templateDocument += r"\end{invoice}"+"%\n"

    templateDocument += "Please include the invoice number on your check. %\n"

    templateDocument += r"\end{letter}%"+"\n"
    templateDocument += r"\end{document}%"+"\n"

    template = templatePreamble+templateHeader+templateDocument

    with open(filename, "w") as f1:
        f1.write(template+"\n")


template = createInvoiceTemplate("invoicePython.tex", data)

