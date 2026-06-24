import os
import shutil

def copy_project():
    src_dir = r"E:\Projeler\MeteorGaleri"
    dst_dir = r"E:\Projeler\filistin_eticaret_projesi"
    
    # Exclude directories
    exclude_dirs = {
        '.git', 'bin', 'obj', 'node_modules', '.claude', '.vscode', '.dotnet-cli', 
        '.dotnet-home', '.dotnet_home', '.dotnetcli', '.playwright-mcp', 
        'db-backups', 'deploy', '_ProjDökümanveScriptler', 'veriler', 
        'yeni_tasarım_stili', 'scratch', 'node_modules'
    }
    
    # Exclude file extensions
    exclude_exts = {'.webp', '.dump', '.sql', '.log', '.png', '.jpg', '.jpeg', '.mp4'}
    
    # Exclude specific files
    exclude_files = {'anasayfa-test.png', 'canvasia-anasayfa.png', 'desktop-nav.png', 'dropdown-hover.png', 'error-screenshot.png', 'fatura-form.png', 'favori-test.png', 'final-nav-1280.png', 'homepage-3sliders.png', 'homepage-final.png', 'homepage-full.png', 'homepage-slider-2.png', 'homepage-slider.png', 'homepage-top.jpeg', 'homesections-edit.png', 'iletişim_sayfası_hata.png', 'modal-screenshot.png', 'nav-1280.png', 'nav-1366.png', 'nav-check.png', 'nav-final-1366.png', 'nav-final-1920.png', 'nav-final.png', 'nav-overflow-1024.png', 'nav-overflow-1366.png', 'nav-smart-overflow.png', 'page-2026-05-23-homepage.png', 'page-screenshot.png', 'screenshot.png'}

    print(f"Starting copy from {src_dir} to {dst_dir}...")
    
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"Created destination directory: {dst_dir}")
        
    copied_count = 0
    ignored_count = 0
    
    for root, dirs, files in os.walk(src_dir):
        # Filter directories to not recurse into excluded ones
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Calculate destination folder
        rel_path = os.path.relpath(root, src_dir)
        dest_folder = os.path.join(dst_dir, rel_path) if rel_path != '.' else dst_dir
        
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            
            # Check exclusions
            if ext in exclude_exts or file in exclude_files:
                ignored_count += 1
                continue
                
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_folder, file)
            
            try:
                shutil.copy2(src_file, dst_file)
                copied_count += 1
            except Exception as e:
                print(f"Failed to copy {src_file}: {e}")
                
    print(f"Copy completed! Copied {copied_count} files, ignored {ignored_count} files.")

if __name__ == "__main__":
    copy_project()
