# Independent Zipper

Simple Python script that zips a directory into independently extracteable zip files of a given size (approximately).

## Usage

Take the folder `my_folder` and compress it into zip files of around 1000MB:

```
python3 independent-zipper.py --input-path my_folder --output_path zips --max-size 1000
```

The output of this script looks like this:

```
part0.zip
part1.zip
part2.zip
...
```

Each zip file can be extracted independentaly. 

## Notes

A few things to note about this script:

* This is a very naive implementation. It goes over all files in the `--input-path` and adds them to a zip file until it has processed the maximum amount of megabytes. At that point it will create a new zip file and keep going.

* Zip files can be smaller than the `--max-size`. That's because the script only looks at the original file size, not the compressed size. So highly-compressible data will yield smaller than expected zip files.

* Zip files can be larger than expected if an individual file exceed `--max-size`. 