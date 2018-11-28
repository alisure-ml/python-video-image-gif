## Python GIF
> 2017-06-20 02:55:02

### 限制条件
* MD...必须2.x才可以
* 目前，图片大小必须相同

### 需要安装
* `import Pillow`
* `import images2gif-Pillow`


### 修改

```
    def writeGifToFile(self, fp, images, durations, loops, xys, disposes):
        palettes, occur = [], []
        for im in images:
            # palettes.append( getheader(im)[1] )  # For PIL
            palettes.append(im.palette.getdata()[1])  # For Pillow
        for palette in palettes:
            occur.append( palettes.count( palette ) )
```