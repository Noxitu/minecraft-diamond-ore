Generated seeds between `1` and `12` using 1.17 and 1.16.5. For each seed server was started, generated initial 23x23 chunks and then stopped.

On my laptop it took about 2 minutes to process single seed.

# 1.17
![Distribution in 1.17](docs/1.17.png)

#### Raw data

    [   0  394  788 1189 1608 1859 1760 1850 1895 1754 1851 1864 1711 1704 1669 1010  251    0    0    0]

Total of 23157 diamonds.

# 1.16.5
![Distribution in 1.16.5](docs/1.16.5.png)

#### Raw data

    [   0  434  806 1171 1673 2120 2008 2044 2047 2162 2025 1965 2074 1841  840  134    0    0    0    0]

Total of 23344 diamonds.

# Required files:
### /jars/minecraft_server.{version}.jar
Download from https://www.minecraft.net/en-us/download/server

### /noxitu/minecraft/map/blocks.json
Generate using `java -cp minecraft_server.jar net.minecraft.data.Main --all`
Read more: https://wiki.vg/Data_Generators

# Important missing features:
 - There is no timeout for generation; I am pretty certain that if you were to run it long enough it would get stuck on generation,
 - Maybe increasing server view distance would increase size of initial world generation,
 - Probably running in offline mode makes more sense.