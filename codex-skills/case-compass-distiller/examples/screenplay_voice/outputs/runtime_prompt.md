# 案例罗盘 1.1｜四层迁移运行单

## 当前任务
写一个双人悬疑场景：调查员在废弃仓库找到同伴留下的手机，另一人坚持同伴已经叛变。场景末尾手机突然收到一条来自现场的消息。

覆盖度：PARTIAL_FIT

## 四层局部先例

只迁移可观察到的局部特征；不得复制原句，不得假装复原某个人。

### structure
- case-003｜虚构场景3｜接近度 0.702｜{"phase_slots":["opening","development","change","payoff"],"paragraph_count":4,"pace_observation":"avg_paragraph_chars=15.75","turn_observation":"后半段出现一条改变判断的新证据"}
- case-002｜虚构场景2｜接近度 0.696｜{"phase_slots":["opening","development","change","payoff"],"paragraph_count":5,"pace_observation":"avg_paragraph_chars=13.4","turn_observation":"后半段出现一条改变判断的新证据"}

### voice
- case-003｜虚构场景3｜接近度 0.681｜{"observable_marks":["sentence_band=short","rhythm=steady","questions_per_100=0.0","exclaims_per_100=0.0","ellipsis_per_100=0.0"],"sentence_band":"short","rhythm_shape":"steady","manual_notes":["短句为主","解释少于反应","关键句单独成轮"]}
- case-002｜虚构场景2｜接近度 0.676｜{"observable_marks":["sentence_band=short","rhythm=mixed","questions_per_100=1.4925","exclaims_per_100=0.0","ellipsis_per_100=0.0"],"sentence_band":"short","rhythm_shape":"mixed","manual_notes":["短句为主","解释少于反应","关键句单独成轮"]}

### dialogue
- case-003｜虚构场景3｜接近度 0.749｜{"observable_marks":["density=medium","turns=2","avg_turn_chars=6.0"],"dialogue_density":"medium","manual_notes":["问句推动信息","回答经常只给半步","动作承担未说出口的信息"]}
- case-002｜虚构场景2｜接近度 0.740｜{"observable_marks":["density=high","turns=4","avg_turn_chars=9.75"],"dialogue_density":"high","manual_notes":["问句推动信息","回答经常只给半步","动作承担未说出口的信息"]}

### interaction
- case-003｜虚构场景3｜接近度 0.737｜{"observable_marks":["speakers=2","alternation=1.0","reaction_order=source_observation_required"],"speaker_count":2,"manual_notes":["一人试探，一人收紧信息","新证据出现后权力位置变化"]}
- case-002｜虚构场景2｜接近度 0.728｜{"observable_marks":["speakers=2","alternation=1.0","reaction_order=source_observation_required"],"speaker_count":2,"manual_notes":["一人试探，一人收紧信息","新证据出现后权力位置变化"]}

## 差异迁移单
- KEEP: 保留本案例已观察到的结构关系，不复制具体措辞
- REPLACE: 题材、人物、事实、数据和全部具体表达
- ADD: 无
- REMOVE: 无
- WATCH: 长句复刻；把单个案例当作普遍结论；只迁移观察到的关系，不携带领航案例的题材和原句

## 生成顺序
1. 先用 structure 先例确定信息顺序和转折位置。
2. 再用 interaction 先例安排谁推动、谁反应、关系如何变化。
3. 用 dialogue 先例控制轮次、问答、打断和潜台词密度。
4. 最后用 voice 先例调整句长、停顿、标点和整体节奏。
5. 全部人物、事实、题材、比喻和具体措辞按当前任务重新写。
6. 输出完成品后，自检是否只继承了局部特征而没有拼贴来源。

## 当前硬要求
必须包含：手机；来自现场的消息
必须避免：直接揭晓叛变真相；长篇解释

## 输出
只输出可直接使用的成品。
