""" DeployScript.py: Copies a deployment directory (only binaries and .aspx 
files for an ASP.NET Visual Studio 2008 solution. Pulls .dll files and .exe 
files from Batch projects within the solution. Ignores .config files, which 
must be placed manually. Can also copy a full directory or delete a full 
directory."""

__author__ = "Bryan Alcorn"
__email__ = "Bryan.C.Alcorn@gmail.com"
__version__="1.0"
__status__="Development"
__date__="10/15/2010"

from shutil import copytree
from shutil import ignore_patterns
from shutil import rmtree
from shutil import move
from Tkinter import *
from tkFileDialog import askdirectory
import os

class mywidgets:
    def __init__(self,root):
        frame=Frame(root);
        self.makeFileDialog(frame);
        frame.pack();
        return
    #defines the text area
    def txtfr(self,frame):
        textfr = Frame(frame);
        textfr.pack(side = TOP);
        return
    #defines GUI
    def makeFileDialog(self,frame):
        CopyFromFrame = Frame(frame);
        self.CopyFromText = Text(CopyFromFrame,height = 1,width = 50,background='gray');
        self.CopyFromText.pack(side = LEFT);
        button = Button(CopyFromFrame,text='From',command=self.dir_open);
        button.pack(side = RIGHT);
        CopyFromFrame.pack(side = TOP);

        CopyButtonFrame = Frame(frame);
        button3 = Button(CopyButtonFrame,text='Delete Directory',command=self.dir_del);
        button3.pack(side=RIGHT);
        button = Button(CopyButtonFrame,text='Copy Deployment Directory',command=self.dir_deploy);
        button.pack(side=RIGHT);
        button2 = Button(CopyButtonFrame,text='Copy Directory',command=self.dir_copy);
        button2.pack(side=LEFT);
        CopyButtonFrame.pack(side = BOTTOM);
        
        CopyToFrame = Frame(frame);
        self.CopyToText = Text(CopyToFrame,height = 1,width = 50,background='white');
        self.CopyToText.pack(side = LEFT);
        button = Button(CopyToFrame,text='To',command=self.dir_open2);
        button.pack(side = RIGHT);
        CopyToFrame.pack(side = BOTTOM);
        return
    #Gets the path for the chosen directory
    def dir_open(self):
        root = self;
        dirname = askdirectory();
        self.CopyFromText.delete(1.0,END);
        self.CopyToText.delete(1.0,END);
        self.CopyFromText.insert(END,dirname);
        self.CopyToText.insert(END,dirname);
    #Gets the path for the second chosen directory   
    def dir_open2(self):
        root = self;
        dirname = askdirectory();
        self.CopyToText.delete(1.0,END);
        self.CopyToText.insert(END,dirname);
        print "Success!"
    #Copies the directory ignoring different file-types  
    def dir_deploy(self):
        fromdir = self.CopyFromText.get(0.0,END).rstrip("\n*.");
        todir = self.CopyToText.get(0.0,END).rstrip("\n*.");
        allDirs = os.listdir(fromdir);
        batchDirs = [];
        for i in allDirs:
            if(i.find("Batch") == 0):
                batchDirs.append(i);
        print "Copying: " + fromdir + "/KPERSSite to " + todir;
        copytree(fromdir + "/KPERSSite",todir,ignore=ignore_patterns('*.cs','*.vspscc','*.user','*.scc','*.csproj','*.config', '*.pdb', "*.vshost"));
        print "Copying Batch Files:";
        for i in batchDirs:
            currentDir = fromdir + "/" + i + "/bin/Debug/";
            batchFiles = os.listdir(currentDir);
            for j in batchFiles:
                if(j[len(j) - 3:len(j)] == "pdb"):
                    pass;
                elif(j[len(j) - 6:len(j)] == "config"):
                    pass;
                elif(j[len(j) - 8:len(j)] == "manifest"):
                    pass;
                elif(j[len(j) - 10:len(j)] == "vshost.exe"):
                    pass;
                elif(j in os.listdir(todir + "/bin/")):
                    pass;
                else:
                    print "Moving: " + j;
                    move(currentDir + "/" + j, todir + "/bin/");
        print "Success!"
    #copies the directory fully
    def dir_copy(self):
        fromdir = self.CopyFromText.get(0.0,END);
        todir = self.CopyToText.get(0.0,END);
        copytree(fromdir[0:len(fromdir)-1],todir[0:len(todir)-1]);
        print "Success!"
    def dir_del(self):
        deldir = self.CopyFromText.get(0.0,END);
        rmtree(deldir[0:len(deldir)-1]);
        print "Success!"
        
def main():
    root = Tk()
    k = mywidgets(root)
    root.title('Copy-Deploy')
    root.mainloop()
main()
