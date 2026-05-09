with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Program.cs', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'app.UseStaticFiles();\r\n'
new = 'app.UseStaticFiles();\r\n\r\n// Ozel Hata Sayfalari (404 vb.) - Guzel tasarimli sayfa gosterir\r\napp.UseStatusCodePagesWithReExecute(\"/Hata/{0}\");\r\n'

if old in content:
    content = content.replace(old, new, 1)
    with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Program.cs', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Done - middleware eklendi')
else:
    # Try with just \n
    old2 = 'app.UseStaticFiles();\n'
    new2 = 'app.UseStaticFiles();\n\n// Ozel Hata Sayfalari (404 vb.) - Guzel tasarimli sayfa gosterir\napp.UseStatusCodePagesWithReExecute("/Hata/{0}");\n'
    if old2 in content:
        content = content.replace(old2, new2, 1)
        with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Program.cs', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Done (LF version) - middleware eklendi')
    else:
        print('Not found - neither version matched')
