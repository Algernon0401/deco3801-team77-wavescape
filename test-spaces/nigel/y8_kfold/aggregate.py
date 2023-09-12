# Define a list of results_dict dictionaries
large_results = [
    {
        "model": "large",
        "fold": 0,
        "metrics/precision": 0.9305511092122836,
        "metrics/recall": 0.7602137140769374,
        "metrics/mAP50": 0.8715824310799278,
        "metrics/mAP50-95": 0.5961292301885706,
        "fitness": 0.6236745502777064,
    },
    {
        "model": "large",
        "fold": 1,
        "metrics/precision": 0.8966055633472142,
        "metrics/recall": 0.752444989597117,
        "metrics/mAP50": 0.836500570597326,
        "metrics/mAP50-95": 0.568460750640958,
        "fitness": 0.5952647326365949,
    },
    {
        "model": "large",
        "fold": 2,
        "metrics/precision": 0.9066490460257164,
        "metrics/recall": 0.8324475908192579,
        "metrics/mAP50": 0.9127557086227003,
        "metrics/mAP50-95": 0.6550502903043485,
        "fitness": 0.6808208321361836,
    },
    {
        "model": "large",
        "fold": 3,
        "metrics/precision": 0.9078379372933786,
        "metrics/recall": 0.6855812725665437,
        "metrics/mAP50": 0.7963223281314376,
        "metrics/mAP50-95": 0.5370693448969417,
        "fitness": 0.5629946432203913,
    },
    {
        "model": "large",
        "fold": 4,
        "metrics/precision": 0.874082413737445,
        "metrics/recall": 0.7835621113470705,
        "metrics/mAP50": 0.8664991747997628,
        "metrics/mAP50-95": 0.5731790587447106,
        "fitness": 0.6025110703502159,
    },
]

medium_results = [
    {
        "model": "medium",
        "fold": 0,
        "metrics/precision": 0.9204968569460493,
        "metrics/recall": 0.8396295643571456,
        "metrics/mAP50": 0.92567811376608,
        "metrics/mAP50-95": 0.6671407808470142,
        "fitness": 0.6929945141389208,
    },
    {
        "model": "medium",
        "fold": 1,
        "metrics/precision": 0.9632321351804811,
        "metrics/recall": 0.8551285096984588,
        "metrics/mAP50": 0.9267065371892548,
        "metrics/mAP50-95": 0.6991318649147727,
        "fitness": 0.721889332142221,
    },
    {
        "model": "medium",
        "fold": 2,
        "metrics/precision": 0.9423839753465081,
        "metrics/recall": 0.8168791296879804,
        "metrics/mAP50": 0.9076193435082204,
        "metrics/mAP50-95": 0.6499336435792094,
        "fitness": 0.6757022135721105,
    },
    {
        "model": "medium",
        "fold": 3,
        "metrics/precision": 0.9038192737213459,
        "metrics/recall": 0.8509068852119178,
        "metrics/mAP50": 0.9120971326322935,
        "metrics/mAP50-95": 0.643986604272115,
        "fitness": 0.6707976571081329,
    },
    {
        "model": "medium",
        "fold": 4,
        "metrics/precision": 0.9742948519893458,
        "metrics/recall": 0.8285027911564442,
        "metrics/mAP50": 0.9095198158253353,
        "metrics/mAP50-95": 0.6285886523480722,
        "fitness": 0.6566817686957984,
    },
]

small_results = [
    {
        "model": "small",
        "fold": 0,
        "metrics/precision": 0.9229362622130213,
        "metrics/recall": 0.8430748068348729,
        "metrics/mAP50": 0.9203068136814783,
        "metrics/mAP50-95": 0.6669857887128577,
        "fitness": 0.6923178912097199,
    },
    {
        "model": "small",
        "fold": 1,
        "metrics/precision": 0.9607873980296555,
        "metrics/recall": 0.7907350286055523,
        "metrics/mAP50": 0.8942117117804302,
        "metrics/mAP50-95": 0.6261681767750381,
        "fitness": 0.6529725302755773,
    },
    {
        "model": "small",
        "fold": 2,
        "metrics/precision": 0.9215012049516973,
        "metrics/recall": 0.847530994211513,
        "metrics/mAP50": 0.9145432618610171,
        "metrics/mAP50-95": 0.6656931459396674,
        "fitness": 0.6905781575318024,
    },
    {
        "model": "small",
        "fold": 3,
        "metrics/precision": 0.9120655111407587,
        "metrics/recall": 0.8036325251365599,
        "metrics/mAP50": 0.8767171217562816,
        "metrics/mAP50-95": 0.5957291761783691,
        "fitness": 0.6238279707361604,
    },
    {
        "model": "small",
        "fold": 4,
        "metrics/precision": 0.9301201006153862,
        "metrics/recall": 0.8425107425429724,
        "metrics/mAP50": 0.9064056641325089,
        "metrics/mAP50-95": 0.6447985388806711,
        "fitness": 0.6709592514058549,
    },
]

nano_results = [
    {
        "model": "nano",
        "fold": 0,
        "metrics/precision": 0.9058461853840996,
        "metrics/recall": 0.7920735740796513,
        "metrics/mAP50": 0.8810041220069418,
        "metrics/mAP50-95": 0.6069263688498526,
        "fitness": 0.6343341441655616,
    },
    {
        "model": "nano",
        "fold": 1,
        "metrics/precision": 0.936906064851897,
        "metrics/recall": 0.8147700706544518,
        "metrics/mAP50": 0.9004443455147809,
        "metrics/mAP50-95": 0.6309358706945065,
        "fitness": 0.657886718176534,
    },
    {
        "model": "nano",
        "fold": 2,
        "metrics/precision": 0.942315964455429,
        "metrics/recall": 0.8263470908078262,
        "metrics/mAP50": 0.9132437022797983,
        "metrics/mAP50-95": 0.6716448572179439,
        "fitness": 0.6958047417241293,
    },
    {
        "model": "nano",
        "fold": 3,
        "metrics/precision": 0.8608252813608891,
        "metrics/recall": 0.8313490922028687,
        "metrics/mAP50": 0.8830804044561799,
        "metrics/mAP50-95": 0.6157734808871561,
        "fitness": 0.6425041732440585,
    },
    {
        "model": "nano",
        "fold": 4,
        "metrics/precision": 0.8873394254908606,
        "metrics/recall": 0.8306321177174989,
        "metrics/mAP50": 0.8915647379355204,
        "metrics/mAP50-95": 0.6095346721981255,
        "fitness": 0.637737678771865,
    },
]


all_results = [large_results, medium_results, small_results, nano_results]


def average_result(attribute):
    total = 0

    for size_result in all_results:
        for result in size_result:
            total = total + result[f"{attribute}"]

        average = total / len(size_result)
        total = 0
        print(f"Average '{attribute}' score for : ", average)


average_result("metrics/precision")
average_result("metrics/recall")
average_result("metrics/mAP50")
average_result("metrics/mAP50-95")
average_result("fitness")


# for size_result in all_results:
#     for result in size_result:
#         total_fitness = total_fitness + result["fitness"]

#     average_fitness = total_fitness / len(size_result)
#     total_fitness = 0

#     print(average_fitness)
