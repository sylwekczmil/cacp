import subprocess
import typing
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import typing_extensions
from sklearn.metrics import accuracy_score

CLASSIFIER_DIR = Path(__file__).parent.joinpath("dist").joinpath("algorithm")
CLASSIFIER_METHODS_DIR = CLASSIFIER_DIR.joinpath("methods")

AVAILABLE_CLASSIFIERS_NAMES = typing_extensions.Literal[
    'Bojarczuk_GP-C', 'Falco_GP-C', 'Tan_GP-C', 'LDA-C', 'QDA-C', 'Kernel-C', 'LinearLMS-C',
    'PolQuadraticLMS-C', 'Logistic-C', 'NB-C', 'Chi-RW-C', 'WF-C', 'FH-GBML-C', 'GFS-Selec-C',
    'NSLV-C', 'SLAVEv0-C', 'SLAVE2-C', 'GFS-GCCL-C', 'GFS-ES-C', 'GP_COACH-C', 'IVTURS-C',
    'MOGUL-C', 'SGERD-C', 'GFS-AdaBoost-C', 'GFS-LogitBoost-C', 'GFS-GPG-C', 'GFS-GP-C', 'GFS-MaxLogitBoost-C',
    'GFS-SP-C', 'FURIA-C', 'PDFC-C', 'MLP-BP-C', 'MLP-CG-C', 'EvRBFN-C', 'RBFN-C',
    'Incr-RBFN-C', 'Decr-RBFN-C', 'LVQ-C', 'C_SVM-C', 'NU_SVM-C', 'SMO-C', 'C45-C',
    'C45_Binarization-C', 'AdaBoost.NC-C', 'CART-C', 'SLIQ-C', 'GAssist-Intervalar-C', 'GAssist-ADI-C', 'OlexGA-C',
    'XCS-C', 'UCS-C', 'GIL-C', 'DMEL-C', 'OIGA-C', 'ILGA-C', 'CORE-C',
    'COGIN-C', 'OCEC-C', 'DT_GA-C', 'DT_Oblique-C', 'Target-C', 'LogenPro-C', 'GANN-C',
    'SONN-C', 'Ensemble-C', 'NNEP-C', 'iRProp+-C', 'PGIRLA-C', 'Hider-C', 'AQ-C',
    'SIA-C', 'RMini-C', 'CN2-C', 'PRISM-C', '1R-C', 'EACH-C', 'EHS_CHC-C',
    'RISE-C', 'BNGE-C', 'INNER-C', 'Riona-C', 'Ripper-C', 'Slipper-C', 'C45Rules-C',
    'C45RulesSA-C', 'PART-C', 'LEM1-C', 'LEM2-C', 'Ritio-C', 'Rules6-C', 'SRI-C',
    'Swap1-C', 'ART-C', 'DataSqueezer-C', 'Ant_Miner-C', 'Advanced_Ant_Miner-C', 'Ant_Miner_Plus-C',
    'Advanced_Ant_Miner_Plus-C', 'PSO_ACO-C', 'ID3-C', 'FuzzyKNN-C', 'IT2FKNN-C', 'CFKNN-C', 'PFKNN-C', 'GAFuzzyKNN-C',
    'IFV_NP-C', 'VWFuzzyKNN-C', 'FuzzyNPC-C', 'JFKNN-C', 'FCMKNN-C', 'D_SKNN-C', 'IFSKNN-C',
    'IF_KNN-C', 'FENN-C', 'PosIBL-C', 'FRKNNA-C', 'FRNN-C', 'FRNN_FRS-C', 'FRNN_VQRS-C',
    'EF_KNN_IVFS-C', 'KNN-C', 'NM-C', 'KNNAdaptive-C', 'CamNN-C', 'CenterNN-C', 'KSNN-C',
    'IDIBL-C', 'KStar-C', 'CPW-C', 'PW-C', 'CW-C', 'DE-C', 'SADE-C',
    'JADE-C', 'OBDE-C', 'DEGL-C', 'SFLSDE-C', 'IPLDE-C', 'SSMASFLSDE-C', 'SSMAPSO-C',
    'SSMALVQ3-C', 'DROP3SFLSDE-C', 'DROP3PSO-C', 'DROP3LVQ3-C', 'ICFSFLSDE-C', 'ICFPSO-C', 'ICFLVQ3-C',
    'NSC-C', 'LBR-C', 'Deeps-C', 'DeepsNN-C', 'CPSO-C', 'LDWPSO-C', 'REPSO-C',
    'PSOLDA-C', 'BioHEL-C', 'MPLCS-C', 'PUBLIC-C', 'FunctionalTrees-C', 'LazyDT-C', 'Fuzzy-FARCHD-C',
    'CBA-C', 'CBA2-C', 'CPAR-C', 'CMAR-C', 'FCRA-C', 'CFAR-C', 'Depur-C',
    'PSO-C', 'RSP-C', 'AMPSO-C', 'PSCSA-C', 'POC-NN-C', 'MSE-C', 'ICPL-C',
    'SGP-C', 'ENPC-C', 'MixtGauss-C', 'LVQTC-C', 'LVQPRU-C', 'HYB-C', 'BTS3-C',
    'GENN-C', 'Chen-C', 'MCA-C', 'GMCA-C', 'DSM-C', 'VQ-C', 'AVQ-C',
    'LVQ1-C', 'LVQ2-C', 'LVQ2_1-C', 'LVQ3-C', 'PNN-C', 'CNN-C', 'ENN-C',
    'RNN-C', 'SNN-C', 'TCNN-C', 'AllKNN-C', 'Multiedit-C', 'MNV-C', 'Shrink-C',
    'IB3-C', 'RMHC-C', 'MCS-C', 'ModelCS-C', 'VSM-C', 'Explore-C', 'GG-C',
    'RNG-C', 'GGA-C', 'SGA-C', 'MENN-C', 'DROP3-C', 'MCNN-C', 'ICF-C',
    'IKNN-C', 'IGA-C', 'PSRCG-C', 'ZhangTS-C', 'NCNEdit-C', 'CPruner-C', 'CHC-C',
    'PBIL-C', 'POP-C', 'Reconsistent-C', 'ENRBF-C', 'MSS-C', 'ENNTh-C', 'BSE-C',
    'SVBPS-C', 'GCNN-C', 'FCNN-C', 'GA_MSE_CC_FSM-C', 'SSMA-C', 'HMNEI-C', 'NRMCS-C',
    'TRKNN-C', 'PSC-C', 'CCIS-C', 'CoCoIS-C', 'EFS_RPS-C', 'EIS_RFS-C', 'CIW_NN-C', 'IFS_COCO-C'
]

options_type = typing.Union[typing.List[str], None]
numeric_type = typing.Union[int, float, None]
value_type = typing.Union[str, numeric_type]


class ClassifierParameter:
    def __init__(self, name: str, type: str, options: options_type, min: numeric_type, max: numeric_type,
                 default: numeric_type):
        self.name = name
        self.type = type
        self.options = options
        self.min = min
        self.max = max
        self.default = default

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items() if item[1] is not None)
        )

    def __repr__(self):
        return self.__str__()

    def validate(self, value: value_type):
        if self.type == "integer" and type(value) != int:
            raise ValueError(
                f"Parameter {self.name} has invalid value {value}, should have int type"
            )
        elif self.type == "real" and type(value) != float:
            raise ValueError(
                f"Parameter {self.name} has invalid value {value}, should have float type"
            )
        elif self.type == "text" and type(value) != str:
            raise ValueError(
                f"Parameter {self.name} has invalid value {value}, should have str type"
            )
        elif self.type == "list" and value not in self.options:
            raise ValueError(
                f"Parameter {self.name} has invalid value {value}, should have one of {self.options}"
            )
        elif self.min is not None and self.max is not None:
            if value < self.min or value > self.max:
                raise ValueError(
                    f"Parameter {self.name} has invalid value {value}, should be between [{self.min}, {self.max}]"
                )


class Classifier:
    def __init__(self, name: str, parameters_overrides: dict = None, seed: int = 1):
        self.name = name
        self.parameters_overrides = parameters_overrides or {}
        self._parse_data_from_list_file()
        self._parse_data_from_metadata_file()
        self._validate_parameters_overrides()
        self.seed = seed if self.accepts_seed else None
        self.config_file_path: Path = Path()
        self.train_result_file_path: Path = Path()
        self.train_result2_file_path: Path = Path()
        self.test_result_file_path: Path = Path()
        self.additional_result_file_path: Path = Path()
        self.additional_result_file_path2: Path = Path()

    def _parse_data_from_list_file(self):
        methods_file_path = CLASSIFIER_DIR.joinpath("Methods.xml")
        root = ET.parse(methods_file_path).getroot()
        for method_tag in root.findall('method'):
            name = method_tag.find("name").text
            if name == self.name:
                self.name = name
                self.jar_file_name = method_tag.find("jar_file").text
                self.family = method_tag.find("family").text
                input_tag = method_tag.find("input")

                def get_input_value(input_name: str):
                    if input_tag is not None:
                        input_value_tag = input_tag.find(input_name)
                        return input_value_tag.text == "Yes" if input_value_tag is not None else False
                    return False

                self.continuous = get_input_value("continuous")
                self.integer = get_input_value("integer")
                self.nominal = get_input_value("nominal")
                self.missing = get_input_value("missing")
                self.imprecise = get_input_value("imprecise")
                self.multi_class = get_input_value("multiclass")
                self.multi_output = get_input_value("multioutput")
                self.multi_instance = get_input_value("multiinstance")

    def _parse_data_from_metadata_file(self):
        xml_path = CLASSIFIER_METHODS_DIR.joinpath(f"{self.name}.xml")
        root = ET.parse(xml_path).getroot()
        self.full_name = root.find("name").text
        self.accepts_seed = root.find("seed").text == "1"
        self.parameters: typing.List[ClassifierParameter] = []
        self.parameters_by_name: typing.Dict[str, ClassifierParameter] = {}
        for parameter_tag in root.findall('parameter'):
            parameter_name = parameter_tag.find("name").text
            parameter_type = parameter_tag.find("type").text
            parameter_default = parameter_tag.find("default").text
            parameter_options = None
            parameter_min = None
            parameter_max = None
            parameter_domain_tag = parameter_tag.find("domain")
            if parameter_type == "list":
                parameter_options = [o.text for o in parameter_domain_tag.findall('item')]
            elif parameter_type == "integer" and parameter_domain_tag:
                parameter_min = int(parameter_domain_tag.find("lowerB").text)
                parameter_max = int(parameter_domain_tag.find("upperB").text)
                parameter_default = int(parameter_default)
            elif parameter_type == "real" and parameter_domain_tag:
                parameter_min = float(parameter_domain_tag.find("lowerB").text)
                parameter_max = float(parameter_domain_tag.find("upperB").text)
                parameter_default = float(parameter_default)
                if parameter_default.is_integer():
                    parameter_default = int(parameter_default)

            parameter = ClassifierParameter(
                name=parameter_name,
                type=parameter_type,
                options=parameter_options,
                min=parameter_min,
                max=parameter_max,
                default=parameter_default
            )
            self.parameters.append(
                parameter
            )
            self.parameters_by_name[parameter.name] = parameter

    def _validate_parameters_overrides(self):
        for parameter_name, parameter_value in self.parameters_overrides.items():
            parameter = self.parameters_by_name.get(parameter_name)
            if parameter is None:
                raise ValueError(f"Parameter {parameter_name} is not valid for Classifier {self.name}")
            else:
                parameter.validate(parameter_value)

    @property
    def jar_file_path(self) -> Path:
        return CLASSIFIER_METHODS_DIR.joinpath(self.jar_file_name)

    def __str__(self):
        ignored = ['parameters_by_name', 'accepts_seed']
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join(f'{name}={value}' for name, value
                      in vars(self).items() if value is not None and name not in ignored)
        )

    def __repr__(self):
        return self.__str__()

    def fit_predict(self,
                    result_file_path: Path,
                    train_file_path: Path, test_file_path: Path,
                    ):
        result_file_path.mkdir(exist_ok=True, parents=True)
        self.config_file_path = result_file_path.joinpath("config.txt")
        self.train_result_file_path = result_file_path.joinpath("result.tra")
        self.test_result_file_path = result_file_path.joinpath("result.tst")
        self.additional_result_file_path = result_file_path.joinpath("result.txt")
        self.additional_result_file_path2 = result_file_path.joinpath("result2.txt")

        def path_to_keel_format(path: Path):
            return str(path).replace('\\', '/')

        lines = [
            f"algorithm = {self.full_name}",
            f'inputData = "{path_to_keel_format(train_file_path)}" "{path_to_keel_format(train_file_path)}" "{path_to_keel_format(test_file_path)}"',
            f'outputData = "{path_to_keel_format(self.train_result_file_path)}" '
            f'"{path_to_keel_format(self.test_result_file_path)}" '
            f'"{path_to_keel_format(self.additional_result_file_path)}" '
            f'"{path_to_keel_format(self.additional_result_file_path2)}"',
            ''
        ]

        if self.seed is not None:
            lines.append(f'seed = {self.seed}')
        for parameter in self.parameters:
            value = parameter.default
            value_override = self.parameters_overrides.get(parameter.name)
            if value_override is not None:
                value = value_override
            lines.append(f'{parameter.name} = {value}')
        lines.append('')
        content = "\n".join(lines)

        with self.config_file_path.open("wb") as f:
            f.write(bytes(content, "UTF-8"))

        run_command = f"java -jar {path_to_keel_format(self.jar_file_path)} {path_to_keel_format(self.config_file_path)}"
        process = subprocess.Popen(run_command, stdout=subprocess.DEVNULL)
        process.wait()
        if process.returncode != 0:
            raise RuntimeError(f"Error while running classifier {self.name} for config file {self.config_file_path}")

        return self.classification_test_results()

    def classification_test_results(self):
        y_true = []
        y_pred = []
        with self.test_result_file_path.open("r") as f:
            for line in f.readlines():
                if '@' not in line:
                    true, pred = line.split()
                    y_true.append(true)
                    y_pred.append(pred)
        return np.array(y_true), np.array(y_pred)


def all_classifiers() -> typing.List[Classifier]:
    """
    Gets all available classifiers

    :return: all classifiers
    """
    return [
        Classifier(name) for name in typing_extensions.get_args(AVAILABLE_CLASSIFIERS_NAMES)
    ]


if __name__ == '__main__':

    working = [
        Classifier("FURIA-C"),
        Classifier("OCEC-C"),
        Classifier("C45Rules-C"),
        Classifier("C45RulesSA-C"),
        Classifier("1R-C"),
        Classifier("C45-C"),
        Classifier("DT_GA-C"),
        Classifier("EACH-C"),
        Classifier("MPLCS-C"),
        Classifier("OIGA-C"),
        Classifier("AdaBoost.NC-C"),
        Classifier("CART-C"),
        Classifier("DT_Oblique-C"),
        Classifier("FH-GBML-C"),
        Classifier("Chi-RW-C"),
        Classifier("Fuzzy-FARCHD-C"),
        Classifier("Chi-RW-C"),
    ]

    not_working = [
        Classifier("GFS-AdaBoost-C"),
    ]

    failed = []
    for classifier in working:
        print(classifier)
        try:
            y_true, y_pred = classifier.fit_predict(
                Path(f"dist/data/result/{classifier.name}").absolute(),
                Path("dist/data/iris-10-1tra.dat").absolute(), Path("dist/data/iris-10-1tst.dat").absolute(),
            )

            print(classifier.name, classifier.parameters_overrides, accuracy_score(y_true, y_pred))
        except Exception as e:
            failed.append(classifier.name)
            print(classifier.name, 'FAILED')

    print('\n\n')
    print(failed)
