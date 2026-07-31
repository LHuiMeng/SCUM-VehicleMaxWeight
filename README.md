# SCUM Vehicle Max Weight Mod

提升 SCUM 游戏中 14 款载具的货舱负重上限至 **21,474,835,20** (float32 上限 ≈ 21.47 亿 kg)。

## 修改清单

| 类别 | 载具 | 原值 | 修改后 |
|---|---|---|---|
| 🚗 SUV | Laika (莱卡) | 1,000 | 2,147,483,520 |
| 🚗 SUV | Rager | 1,200 | 2,147,483,520 |
| 🚗 SUV | Wolfswagen | 800 | 2,147,483,520 |
| 🚜 拖拉机 | Tractor | 1,000 | 2,147,483,520 |
| 🚜 拖拉机 | Tractor_Carriage (拖车) | 1,000 | 2,147,483,520 |
| 🛻 ATV | RIS | 1,200 | 2,147,483,520 |
| 🛴 手推车 | WheelBarrow_Metal | 350 | 2,147,483,520 |
| ⛵ 船 | Barba | 400 | 2,147,483,520 |
| ⛵ 船 | BigRaft | 400 | 2,147,483,520 |
| ⛵ 船 | SmallRaft | 100 | 2,147,483,520 |
| 🏍️ 摩托 | Cruiser | 100 | 2,147,483,520 |
| 🏍️ 摩托 | SidecarBike | 140 | 2,147,483,520 |
| ✈️ 飞机 | Kinglet_Duster | 120 | 2,147,483,520 |
| ✈️ 飞机 | Kinglet_Mariner | 120 | 2,147,483,520 |

## 跳过的载具

- **Sportbike (运动摩托)**: 源文件无 `MaxContainedWeight` 字段,继承 C++ 默认值
- **Dinghy / CityBike / MountainBike / Dirtbike / SUP / WheelBarrow_Improvised**: 纯 `Item` 类型,无货舱容器

## 安装

把 `Vehicle_MaxWeight.pak` 复制到 `SCUM/Saved/Mods/` 目录,启动游戏即可。

或者运行 `python build_mod.py deploy` (自动定位 `%LOCALAPPDATA%/SCUM/Saved/Mods`)。

## 字段位置

每个 `<载具名>_Item_Container_ES.uasset` 文件中:
- Export[2]: `EntityGridInventoryComponentSetup_0`
- Data[2]: `MaxContainedWeight` (FloatPropertyData)

JSON 字段路径:`Export[2].Data[2].Value` (= 2,147,483,520.0)

## 为什么是 2,147,483,520 (21.47 亿)

`MaxContainedWeight` 是 `FloatPropertyData` (float32)。
- int32 上限 2,147,483,647 不能在 float32 中精确表示
- 2,147,483,520 是 float32 可精确表示的最大整数

## 单位说明

- 物品自身 `Weight` 字段单位是 **克 (g)**
- 货舱 `MaxContainedWeight` 字段单位约 **1 kg/单位**

## 与其他 mod 配合

- [SCUM-ChestMaxWeight](https://github.com/LHuiMeng/SCUM-ChestMaxWeight) — 基地箱子货舱上限
- 两者一起放进 Mods 目录,基地囤货 + 车载运输都无重量限制

## 文件结构

```
Vehicle_MaxWeight.pak        # 部署用 PAK
build_mod.py                 # 构建/部署脚本
README.md                    # 本文件
source/                      # 修改后的源资产
└── SCUM/
    └── Content/
        └── ConZ_Files/
            └── Vehicles/
                ├── Airplane/Duster/Kinglet_Duster_Item_Container_ES.{uasset,uexp,json}
                ├── Airplane/Mariner/Kinglet_Mariner_Item_Container_ES.{uasset,uexp,json}
                ├── ATV/RIS/RIS_Item_Container_ES.{uasset,uexp,json}
                ├── Bike/Motorcycle/Cruiser/Cruiser_Item_Container_ES.{uasset,uexp,json}
                ├── Bike/Motorcycle/SidecarBike/SidecarBike_Item_Container_ES.{uasset,uexp,json}
                ├── Boat/Barba/Barba_Item_Container_ES.{uasset,uexp,json}
                ├── Boat/BigRaft/BigRaft_Item_Container_ES.{uasset,uexp,json}
                ├── Boat/SmallRaft/SmallRaft_Item_Container_ES.{uasset,uexp,json}
                ├── Car/Laika/Laika_Item_Container_ES.{uasset,uexp,json}
                ├── Car/Rager/Rager_Item_Container_ES.{uasset,uexp,json}
                ├── Car/WolfsWagen/Wolfswagen_Item_Container_ES.{uasset,uexp,json}
                ├── Tractor/Tractor_Carriage_Item_Container_ES.{uasset,uexp,json}
                ├── Tractor/Tractor_Item_Container_ES.{uasset,uexp,json}
                └── WheelBarrow/Metal/WheelBarrow_Metal_Item_Container_ES.{uasset,uexp,json}
```

## 重新构建

```bash
# 安装 repak
cargo install repak
# 或下载预编译版本放到 PATH

# 仅打包
python build_mod.py build

# 打包 + 部署
python build_mod.py deploy

# 验证 PAK 内容
python build_mod.py verify
```

## 技术细节

- 游戏引擎: UE4 4.27
- PAK 格式版本: V8B
- 工具链: [UAssetCLI](https://github.com/Allar/ue4-style-guide) + [repak](https://github.com/trumank/repak)
