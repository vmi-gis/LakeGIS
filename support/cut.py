import os.path
import os
import shapefile

def cut_files(sourcedir, filenames, destdir):
    for filename in filenames:
        input_shapefile_path = os.path.join(os.path.abspath(sourcedir), filename)

        reader = shapefile.Reader(input_shapefile_path)
        num_features = len(reader.shapeRecords())

        editor = shapefile.Editor(input_shapefile_path)

        for i in range(0, (num_features / 3) * 2):
            editor.delete(-1)

        output_shapefile_path = os.path.join(os.path.abspath(destdir), filename)
        editor.save(output_shapefile_path)

