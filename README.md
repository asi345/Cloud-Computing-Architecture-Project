# To Run Scripts

## PART 1

### Things to customize

1. Give your own credentials in `cloud-comp-arch-project/part1.yaml` - line 16, `part1.sh` - lines 1, 2
2. `cd` to `Part1` folder in `part1.sh` - line 6

## PART 2

1. When running interferences, do not forget update `nodeSelector` field of each of them in their configuration file.
If we run `Part1` set it to `memcached`, if we run `Part2` set it to `parsec`.
