+++
date = '2026-09-15T06:57:37+08:00'
draft = false
title = 'The Art of Medication Schedule'
description = "吃药是一门学问，但什么时候吃药是一门艺术。"
categories = ["数据"]
tags = ["数据分析", "药学"]
+++

no way. 这就是大数据吗？人的用药习惯，反向体现了人的作息，身心状态，和.. 自律。

以下所有用药数据，截至 2026-09-15 早上。

```echarts {width="auto",height="700px",src="chart/the-art-of-medication-schedule-data-1.json"}
{
title: { text: '我的用药记录总览', left: 'center' },
tooltip: { trigger: 'item', axisPointer: { type: 'cross' }, formatter: (params) => {
  const [date, sec, items] = params.value;
  const header = `
    <div style="font-weight: bold; border-bottom: 1px solid #91d7e3; margin-bottom: 2px;">
      ${echarts.format.encodeHTML(params.seriesName)}
      <span style="font-weight: normal; font-size: 12px; color: #618bf0; margin-left: 6px;">
        ${echarts.format.encodeHTML(date)}
      </span>
    </div>
  `;
  const content = (items || []).map(([info, q]) => `
    <div style="line-height: 1.5;">
      ${echarts.format.encodeHTML(q)}
      <span style="font-style: italic; font-size: 12px; color: #618bf0;">
        ${echarts.format.encodeHTML(info)}
      </span>
    </div>
  `).join('');
  return header + content;
}},

xAxis: { type: 'time', name: '日期', splitLine: { show: true, lineStyle: { type: 'dashed' } }, minInterval: 3600 * 24 * 1000, axisLabel: { formatter: '{yyyy}-{MM}-{dd}', rotate: 90 }, axisPointer: { label: { formatter: (params) => { const date = new Date(params.value); const yyyy = date.getFullYear(); const mm = String(date.getMonth() + 1).padStart(2, '0'); const dd = String(date.getDate()).padStart(2, '0'); return `${yyyy}-${mm}-${dd}`; } } } },
yAxis: { type: 'value', name: '时刻', min: 0, max: 86400 - 1, interval: 10800, axisLabel: { formatter: (second) => { const h = String(Math.floor(second / 3600)).padStart(2, '0'); const m = String(Math.floor((second % 3600) / 60)).padStart(2, '0'); const s = String(Math.floor(second % 60)).padStart(2, '0'); return `${h}:${m}:${s}`; }, }, splitLine: { show: true }, axisPointer: { label: { formatter: (params) => { const h = String(Math.floor(params.value / 3600)).padStart(2, '0'); const m = String(Math.floor((params.value % 3600) / 60)).padStart(2, '0'); const s = String(Math.floor(params.value % 60)).padStart(2, '0'); return `${h}:${m}:${s}`; } } } },
legend: { top: '40px', data: ['抗抑郁药', '心境稳定剂', '抗焦虑/镇静/安眠药', 'HRT类', '补充剂', '其他'] },
grid: { left: '0%', right: '0%', bottom: '16%', top: '10%' },
dataZoom: [ { type: 'slider', xAxisIndex: 0, labelFormatter: (value) => { const date = new Date(value); const yyyy = date.getFullYear(); const mm = String(date.getMonth() + 1).padStart(2, '0'); const dd = String(date.getDate()).padStart(2, '0'); return `${yyyy}-${mm}-${dd}`; }, bottom: '10px' }, { type: 'inside', xAxisIndex: 0 } ],

series: [

{ "name": "-", "type": "scatter", "markLine": { "symbol": "none", "silent": true, "data": [
  { "yAxis": 45000, "label": { "formatter": "12:30\n中午药" } },
  { "yAxis": 77400, "label": { "formatter": "21:30\n晚上药" } }
], "lineStyle": { "color": "red", "type": "dotted" } },

}
]

}
```

> 完整[数据](https://github.com/sb-child/sb-child/tree/main/assets/chart)和[本文代码](https://github.com/sb-child/sb-child/tree/main/content/posts/the-art-of-medication-schedule.md)，[数据加工代码](https://github.com/sb-child/sb-child/tree/main/script)都在仓库，你感兴趣可以点进去观摩。但是原始样本不在仓库里。

看图中的12:30线，这是我通常情况下一定会醒着的线，如果这个点我没吃药.. 说明我作息炸了。

看2月到3月10日，图表里下着**补佳乐**暴风雪。原因1是我主观上或者客观上感觉不够，原因2是我忘了所以补回来。你可以数数我一天炫多少。

因为有过几次维生素C缺乏，我很早就学会了每天炫一些维生素(归类为**补充剂**)，通常会和中午药一起吃，如果嫌烦可以关掉**补充剂**类别。

我还有不知道原因的腹泻的毛病，有时容易得上感冒。这些用药归到了**其他**类别里，碍眼可以关掉。

图表zoom到2026年2月25日，分类只开**抗抑郁药**。在服用**文拉法辛**期间，可见我从 225mg/d 高度不开伞降落... 但是曾经我的作息就像晶振一样稳。看12:30的树枝上趴着一只毛毛虫。然后我好长一段时间没再吃抗抑郁药...

能看到跳水之后我开始疯狂的乱吃药来缓解晕动症和让自己睡着。我顺便停了吃到 900mg/d 的**碳酸锂**。

不过是因为我的医生说我看起来是躁狂，要我立刻停掉**文拉法辛**，那我就赌气直接停了，坚持了两天，送完我朋友去火车站，然后回去我就倒了。

然后就是圈内第二大好吃的糖豆，[**苯二氮䓬**类](https://www.od-wiki.com/Drugs/BZD.html)(BZDs)。第一名是[**普瑞巴林**](https://www.od-wiki.com/Drugs/PR)，但是目前只吃过一粒所以.. 你可以问方块冰棍n55她们。

```echarts {width="auto",height="500px",src="chart/the-art-of-medication-schedule-data-2.json"}
{
title: [ { text: '关于BZDs有多好吃这件事', subtext: '曾经服下这些药时，平均每天在我体内留下的精液量.. 什么?',
left: 'center' }, ],

tooltip: { trigger: 'item', axisPointer: { type: 'shadow' },
  formatter: function (params) {
    if (params.seriesType === 'boxplot') {
      const rowName = params.name; const realData = params.data[6];
      return `<div style="font-weight: bold; border-bottom: 1px solid #91d7e3; margin-bottom: 2px;">${rowName}<span style="font-weight: normal; font-size: 12px; color: #618bf0; margin-left: 6px;">累积剂量</span></div>
        <div>最小值 (Min): ${realData[0]}</div>
        <div>下四分位数 (Q1): ${realData[1]}</div>
        <div>中位数 (Median): ${realData[2]}</div>
        <div>上四分位数 (Q3): ${realData[3]}</div>
        <div>最大值 (Max): ${realData[4]}</div> `; }
    if (params.seriesType === 'scatter') {
      return `<div style="font-weight: bold; margin-bottom: 4px;">${params.name} - 离群点</div>
        <div>异常值: ${params.value[0]}</div>`;
    } } },

// dataZoom: [ { type: 'slider', xAxisIndex: 0 }, { type: 'inside', xAxisIndex: 0 }],

grid: { show: true, left: '0%', right: '0%', bottom: '0%' },

yAxis: { type: 'category', data: ['阿普唑仑', '艾司唑仑', '劳拉西泮', '氯硝西泮', '地达西尼'],
boundaryGap: true, nameGap: 30, splitArea: { show: true }, splitLine: { show: true },
axisLabel: { rotate: 0, formatter: (value) => { return (value == '地达西尼') ? (`${value}\n\n(新型安眠药)`) : value } }, },

xAxis: { type: 'value', name: '相对强度\n(10mg 地西泮)', splitArea: { show: true }, axisLabel: { formatter: '{value}x' } },

series: []
}
```

> - 计算方法是通过服药记录绘制代谢曲线(公式和代谢数据来源 Gemini AI，我数学不好)，然后取峰值，再聚合数据画出 boxplot。
> - 数据体现了我**平常**用多少剂量，以及不正常情况下**o多少**。相对强度仅供放在一起参考，鼠标悬浮在 boxplot 上可以看到原始 mg 值。
> - 所以图中的值会比实际用量偏低，同时因为药物会在体内~~受精~~累积，可见连续用药时，半衰期较长的药物在图表中的数值会~~偏高~~偏正常。

白盒子区域是我最常用的剂量，但是呢，除了**氯硝西泮**之外我都多多少少... o过(盒子右边有很长的活塞)。但我不是方块冰棍n55那种大毒枭。

但是为什么依从性那么好的**地达西尼**，盒子瘦成一根棍，最后我也o了一次.. 我明白了，在7月1号清晨，我没睡着.. 一气之下炫了 5mg，后来没有再吃。我怀疑**地达西尼**就是糖豆，有朋友说它吃了会肌松.. 我没有过，可能是体质问题。

虽然图中的**阿普唑仑**都升天了，但是我还记得有另一个朋友把我刚开到的整瓶共 8mg **阿普唑仑**直接倒嘴里，第二天起床还不算晚，人还挺清醒..

对了，插播一条广告，正在打这行文字的笔记本电脑，的电池**即将爆炸**，这是天大的机会，快来交易！

```echarts {width="auto",height="500px",src="chart/the-art-of-medication-schedule-data-3.json"}
{
title: [ { text: 'BATT/USDT 永续合约 10x', subtext: '电池电量百分比，但是 tuned 在操盘!', left: 'center' }, ],

grid: { show: true, left: '0%', right: '0%', bottom: '15%' },

dataZoom: [ { type: 'slider', xAxisIndex: 0 }, { type: 'inside', xAxisIndex: 0 } ],

yAxis: { type: 'value', name: '价格', min: 0, max: 100, axisLabel: { formatter: (price) => { return `${price} USDT`; } }, },

tooltip: {
trigger: 'axis',axisPointer: { type: 'cross' },
formatter: (params) => {
const [date, value] = params[0].value;
const header = `<div style="font-weight: bold; border-bottom: 1px solid #91d7e3; margin-bottom: 2px;">
${echarts.format.encodeHTML(params[0].seriesName)}
<span style="font-weight: normal; font-size: 12px; color: #618bf0; margin-left: 6px;">
${echarts.format.encodeHTML(date)}
</span></div>`;
const content = `<div style="line-height: 1.5;">价格: ${echarts.format.encodeHTML(value)} USDT</div>`;
return header + content;}},

series: []
}
```

> - **Buy or Sell?** 给你5秒时间。注意：以上不是宁德时代股价。投资有风险，充电需谨慎。
> - 实际上是因为我几块钱买的PD充电器模块，跟电池发生了一点点矛盾，不过你可以赌下充电器先炸还是电池先炸。

睡觉是只有人类才会做的事情，小动物什么的经常睡不好半夜被打死吃掉，所以人类想出个歪念头就是用迷幻药剂把自己放倒然后甘愿自己被别的人类分尸。

但是迷幻药剂，不只有一种，以下是我吃过的迷幻蘑菇：

```echarts {width="auto",height="700px",src="chart/the-art-of-medication-schedule-data-4.json"}
{
title: {
    text: '关于应该几点睡觉这件事', subtext: '时间轴平移半天，凌晨是我的基准线!',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    axisPointer: { type: 'cross' },
    formatter: (params) => {
      if (!params || !params.value) return '';
      const [date, sec, items] = params.value;

      const header = `
        <div style="font-weight: bold; border-bottom: 1px solid #91d7e3; margin-bottom: 2px;">
          ${echarts.format.encodeHTML(params.seriesName)}
          <span style="font-weight: normal; font-size: 12px; color: #618bf0; margin-left: 6px;">
            ${echarts.format.encodeHTML(date)}
          </span>
        </div>
      `;
      const content = (items || []).map(([info, q]) => `
        <div style="line-height: 1.5;">
          ${echarts.format.encodeHTML(q)}
          <span style="font-style: italic; font-size: 12px; color: #618bf0;">
            ${echarts.format.encodeHTML(info)}
          </span>
        </div>
      `).join('');
      return header + content;
    }
  },
  xAxis: {
    type: 'time',
    name: '日期',
    splitLine: { show: true, lineStyle: { type: 'dashed' } },
    minInterval: 3600 * 24 * 1000,
    axisLabel: { formatter: '{yyyy}-{MM}-{dd}', rotate: 90 },
    axisPointer: {
      label: {
        formatter: (params) => {
          const date = new Date(params.value);
          const yyyy = date.getFullYear();
          const mm = String(date.getMonth() + 1).padStart(2, '0');
          const dd = String(date.getDate()).padStart(2, '0');
          return `${yyyy}-${mm}-${dd}`;
        }
      }
    }
  },
  yAxis: {
    type: 'value',
    name: '时刻',
    min: -43200,   // 昨日 12:00:00 (-12 小时)
    max: 43200,    // 今日 12:00:00 (+12 小时)
    interval: 10800, // 每 3 小时划分一个刻度
    axisLabel: {
      formatter: (second) => {
        const isYesterday = second < 0;
        const isZero = second == 0;
        const totalSec = isYesterday ? 86400 + second : second;
        const h = String(Math.floor(totalSec / 3600)).padStart(2, '0');
        const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
        const prefix = isYesterday ? '昨日' : '今日';
        return isZero ? '零点' : `${prefix}${h}:${m}`;
      }
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: (val) => val === 0 ? '#1890ff' : '#e0e0e0',
        width: (val) => val === 0 ? 1.5 : 1
      }
    },
    axisPointer: {
      label: {
        formatter: (params) => {
          const sec = params.value;
          const isYesterday = sec < 0;
          const totalSec = isYesterday ? 86400 + sec : sec;
          const h = String(Math.floor(totalSec / 3600)).padStart(2, '0');
          const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
          const s = String(Math.floor(totalSec % 60)).padStart(2, '0');
          return `${isYesterday ? '昨日' : '今日'}${h}:${m}:${s}`;
        }
      }
    }
  },
  legend: {
    bottom: '40px',
    data: ['阿普唑仑','艾司唑仑','劳拉西泮','氯硝西泮','地达西尼','茶苯海明','莱博雷生','异丙嗪','喹硫平','曲唑酮','右佐匹克隆','佐匹克隆','唑吡坦','扎来普隆','米氮平']
  },
  grid: {
    left: '0%',
    right: '0%',
    bottom: '23%',
    top: '10%'
  },
  dataZoom: [
    {
      type: 'slider',
      xAxisIndex: 0,
      labelFormatter: (value) => {
        const date = new Date(value);
        const yyyy = date.getFullYear();
        const mm = String(date.getMonth() + 1).padStart(2, '0');
        const dd = String(date.getDate()).padStart(2, '0');
        return `${yyyy}-${mm}-${dd}`;
      },
      bottom: '10px'
    },
    { type: 'inside', xAxisIndex: 0 }
  ],
  series: []
}
```

> 你知道为什么有这么多种类吗？因为我的医生们比较天真，总是念叨些我已经吃耐受的药。我差点用上**右美托咪定**([Dexmedetomidine](https://en.wikipedia.org/wiki/Dexmedetomidine))。

...长期吃迷幻药就像吃一辈子同一家拼好饭，不光把价格吃上去了，有些饭还会吃腻，但是不乏有一些精品越吃越嘚劲。反正不得不吃，会饿着。

虽然这一类都是安眠药，但是有时它会用在别的地方 -- 抗焦虑或者镇静效果可能有助于睡眠。从2026年2月6日到19日，两坨毛毛虫在不属于它的底盘整齐的爬行。那是我人生中短暂的感到最舒服的日子，只是前期有点困倦，随着药吃腻，效果就没了，舒服也没了，怎么加量也救不回来。

**苯二氮䓬**类唯一的不足，是我真的什么都不焦虑了，我感到平静。我出门会毫无压力的对着武警拍照，因为没有焦虑驱动还会导致忘吃**补佳乐**。回到开头那张图表你可以看到2月19日之后我吃糖突然变规律了。

**异丙嗪**我只碰过两次，一次是因为我睡不着，另一次也是。它有个称号是“大号喹硫平”，因为有个巨大的debuff会导致接下来的24h自己会变成待宰的~~羔羊~~猫娘，给我造成过外交事故，地铁两次坐过站，再也不碰**异丙嗪**。

**茶苯海明**的故事，本来我想买什么**苯海拉明**，因为当时晕的我淘宝上只能买到这个了。虽然列在图表里但是它也许不应该算作安眠药。因为有次没吃上，我还没下床就吐一地。但是我很轻松的就吃多了，然后人变得比较混乱，是另一种待宰的~~羔羊~~猫娘。

还有一个决定性因素影响我睡眠，就是如果有别人跟我一起睡，我通常不能比ta早睡，不然我要么没法入睡，要么被ta弄醒。所以大概6月中旬之后我过的很惨。

---

ok 写数据分析代码快写烦了，总之以上数据你可以放大细品，如果小圆点重叠在一起你可以简单的隐藏和显示分类来看到背后是什么。

最后截至文章写完，这个仓库还有个分支没合过来，因为后续我在手写合约准备发 NFT，需要在这个网站上加个全新的自定义组件作为前端，敬请期待。
