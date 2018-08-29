import os
import re
import sys

def getExecutionPath(argv):
  if "--workingDir" in argv:
    index = argv.index("--workingDir")
    if index < len(argv) - 1:
      value = argv[len(argv) - 1]
      print("Using workingDir value of " + value + ".")
      return value
    else:
      print("No value provided for parameter --workingDir.")
      return None  
  else:
    return os.path.dirname(os.path.realpath(argv[0]))

EXECUTION_PATH = getExecutionPath(sys.argv)

if EXECUTION_PATH == None:
  print("Could not properly set execution path. Exiting...")
  exit()

phragDirPath = os.path.join(EXECUTION_PATH, "phrag")

if not os.path.isdir(phragDirPath):
  print("Execution path " + EXECUTION_PATH + " does not contain phrag dir. Exiting...")
  exit()

phragDefs = list(filter(lambda x: x, os.listdir(phragDirPath)))

for phragDef in phragDefs:
  phragDefFileNames = os.listdir(os.path.join(EXECUTION_PATH, "phrag", phragDef))
  fileRefs = [dict(path = os.path.join(EXECUTION_PATH, "phrag", phragDef, phragDefFileName), name=phragDefFileName) for phragDefFileName in phragDefFileNames]
 
  templateFileRef = next((fr for fr in fileRefs if fr["name"] == phragDef + "." + "template"), None)

  templateContent = None

  with open(templateFileRef["path"], "r") as file:
    templateContent = file.read()

  if templateContent == None:
    print("Could not read template file. Exiting...")
    exit(1)

  phragMarkers = re.findall('{{.*}}', templateContent)

  phragsFileRefs = [fr for fr in fileRefs if ".template" not in fr["name"] and ".default" not in fr["name"]]

  for phragFileRef in phragsFileRefs:
    defaultFileRef = next((fr for fr in fileRefs if fr["name"] == phragFileRef["name"] + "." + "default"), None)
    phragFileRef["default"] = defaultFileRef


  for phragMarker in phragMarkers:
    bareName = phragMarker.replace("{{", "").replace("}}", "")
    matchingFileRef = next((fr for fr in fileRefs if fr["name"] == bareName), None)
    if matchingFileRef == None:
      continue

    phragFileContent = None

    file = None
    
    try:
      file = open(matchingFileRef["path"], "r")
      phragFileContent = file.read()
      file.close()
    except Error:
      if file is not None:
        file.close()

    if phragFileContent is None or len(phragFileContent) == 0:

      phragDefaultFileContent = None

      if matchingFileRef["default"] is not None:
        with open(matchingFileRef["default"]["path"], "r") as file:
          phragDefaultFileContent = file.read()

      if phragDefaultFileContent is not None:
        phragFileContent = phragDefaultFileContent

    templateContent = templateContent.replace(phragMarker, phragFileContent)

  print("Writing file " + phragDef + "...")
  with open(os.path.join(EXECUTION_PATH, phragDef), "w") as file:
    file.write(templateContent)
  print("Done.")

