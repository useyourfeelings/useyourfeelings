/* 
 * editor interface
 * 
 * 201409300350 xcc
 * 
 */

function MDI(editor){
    this.editor = editor;
    this.doc = editor.session.getDocument();
    
    if(typeof(Storage) !== "undefined") {
        // Code for localStorage/sessionStorage.
        this.canUseStorage = true;
    } else {
        // Sorry! No Web Storage support..
        this.canUseStorage = false;
    }
}

function getAllMethods(object) {
    return Object.getOwnPropertyNames(object).filter(function(property) {
        return true;//typeof object[property] == 'function';
    });
}

MDI.prototype.focus = function (){
    this.editor.focus();
}

MDI.prototype.getSelection = function (){
    return this.editor.getSelection();
}

MDI.prototype.selectAll = function (){
    this.editor.selectAll();
}

MDI.prototype.getSelectedText = function (){
    return this.editor.getSelectedText();
}

MDI.prototype.getSelectionRange = function (){
    return this.editor.getSelectionRange();
}

MDI.prototype.undo = function (){
    this.editor.undo();
    this.editor.focus();
}

MDI.prototype.redo = function (){
    this.editor.redo();
    this.editor.focus();
}

MDI.prototype.doBold = function (){
    //alert(mdi.getSelection());
    //alert(typeof(editor.getSelection()));
    //mdi.selectAll();
    originText = this.getSelectedText();
    var range = this.getSelectionRange();
    
    //cursor = editor.session.remove(range);
    this.editor.session.replace(range, '**' + originText + '**');
    
    range.start.column += 2;
    range.end.column = range.start.column;
    
    editor.getSelection().setSelectionRange(range);
    this.editor.focus();
}

MDI.prototype.addLink = function (isImage){
    var url = prompt("enter url", "http://");
    if(url){
        originText = this.getSelectedText();
        var range = this.getSelectionRange();
        console.log(getAllMethods(range));
        console.log(getAllMethods(range.start));
        
        var replaceText = '';
        var descText = 'link description';
        var imageSign = '';
        
        if(isImage)
            imageSign = '!';
        
        if(this.editor.selection.isEmpty()){
            replaceText = imageSign + '[' + descText + '](' + url + ')';
            this.editor.session.replace(range, replaceText);
            range.start.column += imageSign.length + 1;
            range.end.column = range.start.column + descText.length;
            this.editor.getSelection().setSelectionRange(range);
        }
        else{
            replaceText = imageSign + '[' + originText + '](' + url + ')';
            this.editor.session.replace(range, replaceText);
        }
        
        //cursor = editor.session.remove(range);
        //cursor = this.editor.session.replace(range, '[' + originText + ']');
        //console.log(cursor);
    }
    else{
    }
    
    this.editor.focus();
}

MDI.prototype.addUrl = function (){
    this.addLink(false);
}

MDI.prototype.addImage = function (){
    this.addLink(true);
}

MDI.prototype.newDoc = function (){
    if(confirm("this will destroy the current doc!")){
        this.editor.selectAll();
        
        range = this.editor.getSelectionRange();
        this.editor.session.remove(range);
    }
    else{
    }
    
    this.editor.focus();
}

MDI.prototype.getWholeText = function (){
    return this.editor.getValue();
}

MDI.prototype.setWholeText = function (text){
    this.editor.setValue(text);
}

MDI.prototype.resize = function (){
    this.editor.resize();
}

MDI.prototype.setOnChangeCallback = function (callback){
    editor.on("change", callback);
}

MDI.prototype.setUseWrapMode = function (setting){
    this.editor.getSession().setUseWrapMode(setting);
}

MDI.prototype.setShowPrintMargin = function (setting){
    this.editor.setShowPrintMargin(setting);
}

MDI.prototype.setFontSize = function (setting){
    this.editor.setFontSize(setting);
}

MDI.prototype.setTheme = function (setting){
    this.editor.setTheme(setting);
}

MDI.prototype.setMode = function (setting){
    this.editor.getSession().setMode(setting);
}

MDI.prototype.loadStorageText = function (){
    if(!this.canUseStorage)
        return;
    
    storage = localStorage.getItem("text");
    if(storage && storage != "")
        this.setWholeText(storage);
    
    this.editor.moveCursorTo(0, 0);
    
}

MDI.prototype.saveStorageText = function (){
    if(!this.canUseStorage)
        return;
    
    localStorage.setItem("text", mdi.getWholeText());
}

MDI.prototype.saveStorageState = function (){
    if(!this.canUseStorage)
        return;
    
    this.saveStorageText();
}

MDI.prototype.loadStorageState = function (){
    if(!this.canUseStorage)
        return;
    
    this.loadStorageText();
}