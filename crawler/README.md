# Crawler

For generating labeled data for model training.

Need to [start the securimage server](https://github.com/justin0u0/NTHU-OAuth-Decaptcha/tree/master/securimage) first.

Run the following command to generate 5000 captcha images in the directory `./crawler/data/train`,
the image is indexed from `[baseIndex, baseIndex + dataSize)`,
the label will be generated into a CSV file at `./crawler/data/train/label.csv`.

```bash
go run ./crawler/main.go --dataSize 5000 --baseIndex 5000 --outputDir ./crawler/data/train
```
