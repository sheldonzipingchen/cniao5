/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {

    config.language = 'zh-cn';
    config.uiColor = '#FFFFFF';
    config.enterMode = CKEDITOR.ENTER_BR;
    config.shiftEnterMode = CKEDITOR.ENTER_P;
    config.image_previewText ="";
    config.fontSize_defaultLabel = '16px';
    config.fontSize_sizes='12/12px;14/14px;16/16px;18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;36/36px;48/48px;72/72px'


	config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'tools' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'about' }
	];

    config.toolbar_Full =[
            ['Source','CodeSnippet','-','Save','NewPage','Preview','-','Templates'],
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print', 'SpellChecker', 'Scayt'],
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],

        ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
        ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
        ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
        ['Link','Unlink','Anchor'],
        ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],

        ['Styles','Format','Font','FontSize'],
        ['TextColor','BGColor'],
        ['Maximize', 'ShowBlocks','-']
    ];

    config.toolbar_Minimal = [
        { items: [ 'Bold', 'Italic', 'Underline', 'TextColor', '-', 'RemoveFormat', 'PasteText', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', '-', 'Source', 'Image', 'kityformula','CodeSnippet'] }
    ];

    config.toolbar_editVip = [
        { items: [ 'Bold', 'Italic', 'Underline', 'TextColor', '-', 'RemoveFormat', 'PasteText', '-', 'NumberedList', 'BulletedList'] }
    ];

    config.toolbar_Simple = [
        { items: [ 'Bold', 'Italic', 'Underline','-', 'TextColor','BGColor','Styles','Format','Font','FontSize', '-', 'RemoveFormat', 'PasteText', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink',  '-', 'Smiley','Source','CodeSnippet'] }
    ];

    config.toolbar_Thread = [
        { items: [ 'Bold', 'Italic', 'Underline','TextColor',
            '-','BGColor','FontSize',
            '-',
            'RemoveFormat', 'PasteText',
            '-',
            'NumberedList', 'BulletedList',
            '-',
            'Link', 'Unlink', 'imageupload',
            '-',
            'CodeSnippet','Save',
            '-','Blockquote','HorizontalRule','Maximize','Source'] }
    ];

    config.toolbar_Question = [
        { items: [ 'Bold', 'Italic', 'Underline', 'TextColor', '-', 'RemoveFormat', 'PasteText', '-', 'QuestionBlank', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', '-', 'Source', 'Image', 'CodeSnippet'] }
    ];

    config.toolbar_Group = [
        { items: [ 'Bold', 'Italic', 'Underline', 'TextColor', '-', 'RemoveFormat', 'PasteText', '-', 'Smiley', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', 'Image', '-', 'Source'] }
    ];

    config.toolbar_Detail = [
        { items: [ 'FontSize'] },
        { items: [ 'Bold', 'Italic', 'Underline', 'TextColor', '-', 'RemoveFormat', 'PasteText', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', 'Image', '-', 'Source', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] }
    ];



    config.extraPlugins = 'codesnippet,smiley,font,panelbutton,colorbutton,markdown,imageupload';
    //使用zenburn的代码高亮风格样式 PS:zenburn效果就是黑色背景
    //如果不设置着默认风格为default
    config.codeSnippet_theme= 'zenburn';
    config.codeSnippet_languages= ['java','xml','json','html','javascript','css','makefile','sql','objectivec','php'];

//    config.filebrowserUploadUrl='http://upload.qiniu.com'
};

CKEDITOR.on( 'instanceReady', function( ev ) { with (ev.editor.dataProcessor.writer) {
setRules("p", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("h1", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("h2", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("h3", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("h4", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("h5", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("div", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("table", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("tr", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("td", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("iframe", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("li", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("ul", {indent : false, breakAfterOpen : false, breakBeforeClose : false} );
setRules("ol", {indent : false, breakAfterOpen : false, breakBeforeClose : false} ); }
});
