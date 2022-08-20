style_sheet = """
    QWidget{
        background-color: #FFC000;
    }
    NameBtn{
        color:  #000000;
        border: 5px solid #000000;
        border-radius: 15px;
        background-color: #FFC000;
        text-align: left;
        padding: 3px 10px;
    }
    NameBtn:pressed {
        color:  #C00000;
        border-color: #C00000;
    }
    QToolButton{
        border: 5px solid #000000;
        border-radius: 15px;
        background-color: #FFC000;
    }
    QToolButton:pressed {
        border-color: #C00000;
    }
    QToolButton#close_window{
        background-color: #000000;
        border-radius: 0px;
    }
    QToolButton#close_window:pressed {
        background-color: #C00000;
    }
    BlackBtn{
        color:  #FFC000;
	    border-radius: 15px;
	    background-color: #000000;
        padding: 8px 15px;
    }
    BlackBtn:pressed {
        background-color: #C00000;
    }
    YellowBtn{
        color:  #000000;
	    border-radius: 15px;
	    background-color: #FFC000;
        padding: 8px 15px;
    }
    YellowBtn:pressed {
        background-color: #ED7D00;
    }
    CheckBtn{
        color:  #000000;
        border: 5px solid #000000;
        border-radius: 15px;
        background-color: #FFC000;
        padding: 3px 10px;
    }
    CheckBtn:checked {
        color:  #FFC000;
	    border-radius: 15px;
        border: 0px;
	    background-color: #000000;
        padding: 8px 15px;
    }
    QLineEdit{
        color:  #000000;
        border: 5px solid #000000;
        border-radius: 15px;
        background-color: #FFC000;
        text-align: left;
        padding: 3px 10px;
        font: 75 24pt "Agency FB";
    }
    QLineEdit:read-only {
        border:0px
    }
    QWidget#sub_widget{
        background-color: #000000;
    }
    QLabel{
        background: transparent;
        color: #000000;
    }
    QLabel#yellow_title{
        color: #FFC000;
        font: 75 36pt "Agency FB";
    }
    QScrollArea {
        border: none;
    }
    QScrollBar
    {
        background-color: #000000;
        width: 22px;
        margin: 10px, 0px;
        border: 5px solid #000000;
        border-radius: 11px;
    }
    QScrollBar::handle
    {
        background-color: #FFC000;
        min-height: 5px;
        border-radius: 6px;
    }
    QScrollBar::add-line, QScrollBar::sub-line {
        border: none;
        background: none;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        background: none;
    }
"""