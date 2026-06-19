<?xml version="1.0" encoding="UTF-8"?>
<conceptualSchema version="TJ1.0">
    <databaseConnection>
        <embed url="/E:/_3_Master/Applied-Computational-Intelligence-UBB/Year1_Semester2_KnowledgeDiscovery/FinalProject/ToscanaJScalesProject/Final_Processed_Steel_Data_Clean_Full.sql" />
        <table name="PREPROCESSEDDATASET" />
        <key name="DATETIME_COMBINED" />
    </databaseConnection>
    <queries />
    <diagram title="NominalScale_RULClass">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Medium') AND NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Low') AND NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Healthy') AND NOT (PREPROCESSEDDATASET.RUL_CLASS = 'Critical')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-17.0" y="60.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Critical'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Critical</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="80.5" y="82.5" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Low'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Low</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="33.0" y="50.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Healthy'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Healthy</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="-147.0" y="170.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.RUL_CLASS = 'Medium'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Medium</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="-50.5" y="362.5" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="0" to="1" />
        <edge from="0" to="2" />
        <edge from="0" to="3" />
        <edge from="0" to="4" />
        <edge from="1" to="5" />
        <edge from="2" to="5" />
        <edge from="3" to="5" />
        <edge from="4" to="5" />
        <projectionBase>
            <vector x="80.5" y="82.5" />
            <vector x="33.0" y="50.0" />
            <vector x="-17.0" y="60.0" />
            <vector x="-147.0" y="170.0" />
        </projectionBase>
    </diagram>
    <diagram title="NominalScale_SteelType">
        <node id="0">
            <position x="33.75423812866211" y="200.961181640625" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = '1015'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>1015</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="200.18484497070312" y="197.74978637695312" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = '1018'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>1018</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-207.8710479736328" y="153.6591339111328" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = '25G2S'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>25G2S</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="169.02308654785156" y="19.221195220947266" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.STEEL_TYPE = 'YP') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = 'V500V') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = 'St4sp') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = 'St3sp') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = 'Arm500') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = 'Arm240') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = '25G2S') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = '20') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = '1018') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = '1015') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = '1010') AND NOT (PREPROCESSEDDATASET.STEEL_TYPE = '1008')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="268.15039984385163" y="223.2079532146454" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = '1010'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>1010</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="110.5123578707377" y="194.62124943733218" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = 'Arm500'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Arm500</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="413.34063720703125" y="234.0507049560547" />
            <attributeLabelStyle>
                <offset x="119.1336441040039" y="40.756245613098145" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = 'St3sp'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>St3sp</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="-134.1063092549642" y="158.11614990234378" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = 'V500V'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>V500V</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="161.73135375976562" y="196.32559204101562" />
            <attributeLabelStyle>
                <offset x="51.72908020019531" y="20.37812304496765" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = 'YP'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>YP</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="40.44363784790039" y="288.9619445800781" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="73.43074798583984" y="200.1234588623047" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = '1008'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>1008</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="4.841499636570615" y="196.32515954971316" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = '20'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>20</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="351.10217920939124" y="220.06258392333987" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = 'Arm240'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>Arm240</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="-46.32659800847372" y="197.21264940500262" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.STEEL_TYPE = 'St4sp'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>St4sp</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="3" to="0" />
        <edge from="3" to="1" />
        <edge from="3" to="2" />
        <edge from="3" to="4" />
        <edge from="3" to="5" />
        <edge from="3" to="6" />
        <edge from="3" to="7" />
        <edge from="3" to="8" />
        <edge from="0" to="9" />
        <edge from="1" to="9" />
        <edge from="2" to="9" />
        <edge from="4" to="9" />
        <edge from="5" to="9" />
        <edge from="6" to="9" />
        <edge from="7" to="9" />
        <edge from="8" to="9" />
        <edge from="10" to="9" />
        <edge from="11" to="9" />
        <edge from="12" to="9" />
        <edge from="13" to="9" />
        <edge from="3" to="10" />
        <edge from="3" to="11" />
        <edge from="3" to="12" />
        <edge from="3" to="13" />
        <projectionBase>
            <vector x="80.01168060302734" y="80.00003814697266" />
            <vector x="40.011566162109375" y="40.000152587890625" />
            <vector x="20.0111083984375" y="20.0006103515625" />
            <vector x="10.00927734375" y="10.00244140625" />
            <vector x="5.001953125" y="5.009765625" />
            <vector x="2.47265625" y="2.5390625" />
            <vector x="1.10546875" y="1.40625" />
            <vector x="0.01171875" y="1.25" />
            <vector x="-2.17578125" y="2.8125" />
            <vector x="-9.83203125" y="10.15625" />
            <vector x="-39.91015625" y="40.078125" />
            <vector x="-159.94921875" y="160.0390625" />
        </projectionBase>
    </diagram>
    <diagram title="NominalScale_WorkpieceGeometry">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.WORKPIECE_SLICE_GEOMETRY = '180x180') AND NOT (PREPROCESSEDDATASET.WORKPIECE_SLICE_GEOMETRY = '150x150')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.WORKPIECE_SLICE_GEOMETRY = '180x180'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>180x180</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.WORKPIECE_SLICE_GEOMETRY = '150x150'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>150x150</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="0" to="1" />
        <edge from="1" to="2" />
        <edge from="3" to="2" />
        <edge from="0" to="3" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="NominalScale_AlloyType">
        <node id="0">
            <position x="-108.0" y="200.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.ALLOY_TYPE = 'close'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>close</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-56.0" y="320.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.ALLOY_TYPE = 'close') AND NOT (PREPROCESSEDDATASET.ALLOY_TYPE = 'open')</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.ALLOY_TYPE = 'open'</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>open</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="0" />
        <edge from="0" to="1" />
        <edge from="3" to="1" />
        <edge from="2" to="3" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="NominalScale_StreamIdentifier">
        <node id="0">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>NOT (PREPROCESSEDDATASET.NUM_STREAM = 6) AND NOT (PREPROCESSEDDATASET.NUM_STREAM = 5) AND NOT (PREPROCESSEDDATASET.NUM_STREAM = 4) AND NOT (PREPROCESSEDDATASET.NUM_STREAM = 3) AND NOT (PREPROCESSEDDATASET.NUM_STREAM = 2) AND NOT (PREPROCESSEDDATASET.NUM_STREAM = 1)</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="-51.28125" y="370.78125" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent />
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="0.75" y="20.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.NUM_STREAM = 1</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="-34.25" y="45.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.NUM_STREAM = 4</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>4</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="18.25" y="22.5" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.NUM_STREAM = 2</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="40.125" y="40.625" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.NUM_STREAM = 3</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>3</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="-156.75" y="162.5" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.NUM_STREAM = 6</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>6</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="80.59375" y="80.15625" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>PREPROCESSEDDATASET.NUM_STREAM = 5</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="1" />
        <edge from="3" to="1" />
        <edge from="4" to="1" />
        <edge from="5" to="1" />
        <edge from="6" to="1" />
        <edge from="7" to="1" />
        <edge from="0" to="2" />
        <edge from="0" to="3" />
        <edge from="0" to="4" />
        <edge from="0" to="5" />
        <edge from="0" to="6" />
        <edge from="0" to="7" />
        <projectionBase>
            <vector x="80.59375" y="80.15625" />
            <vector x="40.125" y="40.625" />
            <vector x="18.25" y="22.5" />
            <vector x="0.75" y="20.0" />
            <vector x="-34.25" y="45.0" />
            <vector x="-156.75" y="162.5" />
        </projectionBase>
    </diagram>
    <diagram title="OrdinalScale_ExcludeBounds_Crystallizer">
        <node id="0">
            <position x="-112.0" y="480.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(CAST_IN_ROW&gt;16)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;16</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(CAST_IN_ROW&lt;=8)</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="-56.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>(CAST_IN_ROW&gt;8) AND (CAST_IN_ROW&lt;=16)</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>&gt;8</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="0" />
        <edge from="1" to="2" />
        <projectionBase>
            <vector x="-56.0" y="240.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_RULEncoded_x_WaterCooling">
        <node id="0">
            <position x="818.0364837646538" y="319.1962890625012" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="7">((RUL_CLASS_ENCODED&gt;2)) AND ((CAST_IN_ROW&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="238.01216125488315" y="26.398763020833357" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="2">((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((CAST_IN_ROW&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="1">RUL_CLASS_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="476.0243225097644" y="52.797526041666515" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="11">((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((CAST_IN_ROW&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="4">RUL_CLASS_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="342.01216125488315" y="266.39876302083337" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="5">((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((CAST_IN_ROW&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="6">((RUL_CLASS_ENCODED&lt;=0)) AND ((CAST_IN_ROW&gt;0) AND (CAST_IN_ROW&lt;=1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="3">CAST_IN_ROW &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="580.0243225097644" y="292.7975260416665" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="8">((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((CAST_IN_ROW&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="528.0243225097644" y="172.79752604166652" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="9">((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((CAST_IN_ROW&gt;0) AND (CAST_IN_ROW&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="3">((RUL_CLASS_ENCODED&lt;=0)) AND ((CAST_IN_ROW&gt;1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="2">CAST_IN_ROW &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="714.0364837646538" y="79.1962890625012" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="1">((RUL_CLASS_ENCODED&gt;2)) AND ((CAST_IN_ROW&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute contextPosition="0">RUL_CLASS_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="290.01216125488315" y="146.39876302083337" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="0">((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((CAST_IN_ROW&gt;0) AND (CAST_IN_ROW&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="766.0364837646538" y="199.1962890625012" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="4">((RUL_CLASS_ENCODED&gt;2)) AND ((CAST_IN_ROW&gt;0) AND (CAST_IN_ROW&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object contextPosition="10">((RUL_CLASS_ENCODED&lt;=0)) AND ((CAST_IN_ROW&lt;=0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="10" to="0" />
        <edge from="5" to="0" />
        <edge from="11" to="1" />
        <edge from="1" to="2" />
        <edge from="7" to="3" />
        <edge from="9" to="3" />
        <edge from="11" to="4" />
        <edge from="3" to="5" />
        <edge from="6" to="5" />
        <edge from="2" to="6" />
        <edge from="9" to="6" />
        <edge from="4" to="7" />
        <edge from="2" to="8" />
        <edge from="1" to="9" />
        <edge from="4" to="9" />
        <edge from="6" to="10" />
        <edge from="8" to="10" />
        <projectionBase>
            <vector x="238.01216125488315" y="26.398763020833357" />
            <vector x="238.01216125488122" y="26.398763020833158" />
            <vector x="52.0" y="120.0" />
            <vector x="52.0" y="120.0" />
            <vector x="238.0121612548894" y="26.39876302083468" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_RUL_x_SteelTemperature">
        <node id="0">
            <position x="899.8777465820326" y="116.72867250442704" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="299.9592488606769" y="38.90955750147492" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="1003.8777465820312" y="356.7286725044251" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="951.8777465820312" y="236.7286725044239" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="403.959248860677" y="278.90955750147464" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="651.9184977213561" y="197.81911500294973" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="351.95924886067667" y="158.90955750147518" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="703.9184977213561" y="317.81911500294933" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="599.9184977213545" y="77.81911500295041" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="9" to="0" />
        <edge from="11" to="1" />
        <edge from="11" to="2" />
        <edge from="4" to="3" />
        <edge from="8" to="3" />
        <edge from="0" to="4" />
        <edge from="6" to="4" />
        <edge from="7" to="5" />
        <edge from="10" to="5" />
        <edge from="7" to="6" />
        <edge from="9" to="6" />
        <edge from="1" to="7" />
        <edge from="2" to="7" />
        <edge from="5" to="8" />
        <edge from="6" to="8" />
        <edge from="1" to="9" />
        <edge from="2" to="10" />
        <projectionBase>
            <vector x="-108.0" y="200.0" />
            <vector x="52.0" y="120.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_RUL_x_ResistanceTonn">
        <node id="0">
            <position x="313.73750305175787" y="262.66627502441344" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((RESISTANCE_TONN&gt;12560))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="733.212509155274" y="307.9988250732374" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((RESISTANCE_TONN&gt;12560))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="419.4750061035172" y="45.33255004882659" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((RESISTANCE_TONN&lt;=6280))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="209.73750305175747" y="22.666275024414432" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((RESISTANCE_TONN&lt;=6280))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="523.4750061035163" y="285.33255004882676" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((RESISTANCE_TONN&gt;12560))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((RESISTANCE_TONN&gt;6280) AND (RESISTANCE_TONN&lt;=12560))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RESISTANCE_TONN &gt;6280</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="629.2125091552715" y="67.99882507324537" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((RESISTANCE_TONN&lt;=6280))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="261.7375030517577" y="142.6662750244144" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((RESISTANCE_TONN&gt;6280) AND (RESISTANCE_TONN&lt;=12560))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((RESISTANCE_TONN&lt;=6280))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="681.2125091552734" y="187.99882507324355" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((RESISTANCE_TONN&gt;6280) AND (RESISTANCE_TONN&lt;=12560))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((RESISTANCE_TONN&gt;12560))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RESISTANCE_TONN &gt;12560</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="471.4750061035172" y="165.33255004883154" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((RESISTANCE_TONN&gt;6280) AND (RESISTANCE_TONN&lt;=12560))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="7" to="0" />
        <edge from="10" to="0" />
        <edge from="4" to="1" />
        <edge from="9" to="1" />
        <edge from="3" to="2" />
        <edge from="8" to="3" />
        <edge from="0" to="4" />
        <edge from="11" to="4" />
        <edge from="8" to="5" />
        <edge from="2" to="6" />
        <edge from="3" to="7" />
        <edge from="5" to="7" />
        <edge from="6" to="9" />
        <edge from="11" to="9" />
        <edge from="5" to="10" />
        <edge from="2" to="11" />
        <edge from="7" to="11" />
        <projectionBase>
            <vector x="-108.0" y="200.0" />
            <vector x="52.0" y="120.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_SteelTemperature_x_WaterCooling">
        <node id="0">
            <position x="496.59454345703125" y="279.62384033203125" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="444.59454345703125" y="159.62384033203125" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&gt;0) AND (WATER_CONSUMPTION_LITER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="785.1890869140625" y="79.2476806640625" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>WATER_CONSUMPTION_LITER_MINUTE_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="889.1890869140625" y="319.2476806640625" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=0)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&gt;0) AND (WATER_CONSUMPTION_LITER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>WATER_CONSUMPTION_LITER_MINUTE_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="837.1890869140625" y="199.2476806640625" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;1)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&gt;0) AND (WATER_CONSUMPTION_LITER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="392.59454345703125" y="39.62384033203125" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&gt;0) AND (STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED&lt;=1)) AND ((WATER_CONSUMPTION_LITER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>STEEL_TEMPERATURE_GRAB1_CELSIUS_DEG_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <edge from="2" to="0" />
        <edge from="4" to="0" />
        <edge from="6" to="2" />
        <edge from="8" to="2" />
        <edge from="8" to="3" />
        <edge from="6" to="4" />
        <edge from="0" to="5" />
        <edge from="7" to="5" />
        <edge from="1" to="6" />
        <edge from="2" to="7" />
        <edge from="3" to="7" />
        <edge from="1" to="8" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_CrystalizerMovement_x_SwingFrequency">
        <node id="0">
            <position x="474.60327911376953" y="165.34825134277344" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&gt;0) AND (CRYSTALLIZER_MOVEMENT_MM_ENCODED&lt;=1)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&gt;0) AND (SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="897.2065582275391" y="210.69650268554688" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&gt;1)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&gt;0) AND (SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="949.2065582275391" y="330.6965026855469" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&gt;1)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="845.2065582275391" y="90.69650268554688" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&gt;1)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>CRYSTALLIZER_MOVEMENT_MM_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&lt;=0)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&gt;0) AND (SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="422.60327911376953" y="45.34825134277344" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&gt;0) AND (CRYSTALLIZER_MOVEMENT_MM_ENCODED&lt;=1)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>CRYSTALLIZER_MOVEMENT_MM_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&lt;=0)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="526.6032791137695" y="285.34825134277344" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&gt;0) AND (CRYSTALLIZER_MOVEMENT_MM_ENCODED&lt;=1)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((CRYSTALLIZER_MOVEMENT_MM_ENCODED&lt;=0)) AND ((SWING_FREQUENCY_AMOUNT_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="4" to="0" />
        <edge from="5" to="0" />
        <edge from="0" to="1" />
        <edge from="3" to="1" />
        <edge from="1" to="2" />
        <edge from="7" to="2" />
        <edge from="5" to="3" />
        <edge from="8" to="4" />
        <edge from="8" to="5" />
        <edge from="4" to="6" />
        <edge from="0" to="7" />
        <edge from="6" to="7" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_RULEncoded_x_Stream">
        <node id="0">
            <position x="2381.619201660163" y="275.07125854490755" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&gt;5))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_STREAM &gt;5</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="516.7995707194005" y="701.4510447184241" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&gt;0) AND (NUM_STREAM&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="1190.809600830066" y="137.5356292724639" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&gt;2) AND (NUM_STREAM&lt;=3))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_STREAM &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="873.7817586262955" y="528.760976155601" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&gt;1) AND (NUM_STREAM&lt;=2))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="39.95434570312504" y="218.53527832031287" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="2104.545705159467" y="884.8318837483612" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&gt;4) AND (NUM_STREAM&lt;=5))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="2461.5278930664126" y="712.1418151855353" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&gt;5))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="2501.482238769539" y="930.67709350585" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&gt;5))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="1270.7182922363115" y="574.6061859130874" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&gt;2) AND (NUM_STREAM&lt;=3))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="119.86303710937598" y="655.6058349609394" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="833.8274129231716" y="310.2256978352876" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&gt;1) AND (NUM_STREAM&lt;=2))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="396.9365336100266" y="45.84520975748751" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&gt;0) AND (NUM_STREAM&lt;=1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_STREAM &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="12">
            <position x="1667.6548258463401" y="620.4513956705663" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&gt;3) AND (NUM_STREAM&lt;=4))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="13">
            <position x="1230.763946533188" y="356.07090759277565" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&gt;2) AND (NUM_STREAM&lt;=3))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="14">
            <position x="2024.637013753235" y="447.76132710773595" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&gt;4) AND (NUM_STREAM&lt;=5))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="15">
            <position x="913.7361043294186" y="747.2962544759089" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&gt;1) AND (NUM_STREAM&lt;=2))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="16">
            <position x="79.90869140625037" y="437.07055664062636" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="17">
            <position x="793.8730672200473" y="91.69041951497456" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&gt;1) AND (NUM_STREAM&lt;=2))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_STREAM &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="18">
            <position x="2421.573547363281" y="493.6065368652214" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&gt;5))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>6.0</coordinate>
            </ndimVector>
        </node>
        <node id="19">
            <position x="1707.609171549459" y="838.986673990875" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&gt;3) AND (NUM_STREAM&lt;=4))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="20">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&lt;=0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="21">
            <position x="1310.6726379394395" y="793.1414642333954" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_STREAM&gt;2) AND (NUM_STREAM&lt;=3))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>3.0</coordinate>
            </ndimVector>
        </node>
        <node id="22">
            <position x="436.89087931315134" y="264.38048807780046" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&gt;0) AND (NUM_STREAM&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="23">
            <position x="2064.5913594563526" y="666.2966054280507" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&gt;4) AND (NUM_STREAM&lt;=5))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="24">
            <position x="1984.6826680501144" y="229.2260487874289" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&gt;4) AND (NUM_STREAM&lt;=5))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_STREAM &gt;4</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>5.0</coordinate>
            </ndimVector>
        </node>
        <node id="25">
            <position x="476.8452250162766" y="482.9157663981131" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_STREAM&gt;0) AND (NUM_STREAM&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="26">
            <position x="1627.7004801432188" y="401.91611735025504" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_STREAM&gt;3) AND (NUM_STREAM&lt;=4))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <node id="27">
            <position x="1587.7461344400986" y="183.38083902994504" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_STREAM&gt;3) AND (NUM_STREAM&lt;=4))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_STREAM &gt;3</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>4.0</coordinate>
            </ndimVector>
        </node>
        <edge from="24" to="0" />
        <edge from="9" to="1" />
        <edge from="25" to="1" />
        <edge from="17" to="2" />
        <edge from="10" to="3" />
        <edge from="25" to="3" />
        <edge from="20" to="4" />
        <edge from="19" to="5" />
        <edge from="23" to="5" />
        <edge from="18" to="6" />
        <edge from="23" to="6" />
        <edge from="5" to="7" />
        <edge from="6" to="7" />
        <edge from="3" to="8" />
        <edge from="13" to="8" />
        <edge from="16" to="9" />
        <edge from="22" to="10" />
        <edge from="17" to="10" />
        <edge from="20" to="11" />
        <edge from="8" to="12" />
        <edge from="26" to="12" />
        <edge from="2" to="13" />
        <edge from="10" to="13" />
        <edge from="24" to="14" />
        <edge from="26" to="14" />
        <edge from="1" to="15" />
        <edge from="3" to="15" />
        <edge from="4" to="16" />
        <edge from="11" to="17" />
        <edge from="0" to="18" />
        <edge from="14" to="18" />
        <edge from="21" to="19" />
        <edge from="12" to="19" />
        <edge from="15" to="21" />
        <edge from="8" to="21" />
        <edge from="4" to="22" />
        <edge from="11" to="22" />
        <edge from="14" to="23" />
        <edge from="12" to="23" />
        <edge from="27" to="24" />
        <edge from="22" to="25" />
        <edge from="16" to="25" />
        <edge from="13" to="26" />
        <edge from="27" to="26" />
        <edge from="2" to="27" />
        <projectionBase>
            <vector x="52.0" y="120.0" />
            <vector x="-108.0" y="200.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_RULEncoded_x_Crystallizer">
        <node id="0">
            <position x="803.565724690754" y="233.89069112142045" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_CRYSTALLIZER&gt;8) AND (NUM_CRYSTALLIZER&lt;=16))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="430.93919881184934" y="196.60071055094397" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_CRYSTALLIZER&gt;8) AND (NUM_CRYSTALLIZER&lt;=16))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="1234.5049235026065" y="430.49140167236106" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_CRYSTALLIZER&gt;16))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="745.253051757812" y="74.57996114095033" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_CRYSTALLIZER&lt;=8))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="861.8783976236965" y="393.2014211018881" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((NUM_CRYSTALLIZER&gt;16))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="489.25187174479214" y="355.91144053141335" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_CRYSTALLIZER&gt;16))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_CRYSTALLIZER&lt;=8))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="58.31267293294269" y="159.31072998046864" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_CRYSTALLIZER&gt;8) AND (NUM_CRYSTALLIZER&lt;=16))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;8</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="1176.1922505696632" y="271.1806716918943" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_CRYSTALLIZER&gt;8) AND (NUM_CRYSTALLIZER&lt;=16))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="116.62534586588549" y="318.62145996093795" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((NUM_CRYSTALLIZER&gt;16))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>NUM_CRYSTALLIZER &gt;16</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="372.6265258789064" y="37.289980570475365" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((NUM_CRYSTALLIZER&lt;=8))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="1117.8795776367165" y="111.86994171142499" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((NUM_CRYSTALLIZER&lt;=8))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <edge from="3" to="0" />
        <edge from="7" to="1" />
        <edge from="10" to="1" />
        <edge from="4" to="2" />
        <edge from="8" to="2" />
        <edge from="10" to="3" />
        <edge from="0" to="4" />
        <edge from="5" to="4" />
        <edge from="1" to="5" />
        <edge from="9" to="5" />
        <edge from="6" to="7" />
        <edge from="0" to="8" />
        <edge from="11" to="8" />
        <edge from="7" to="9" />
        <edge from="6" to="10" />
        <edge from="3" to="11" />
        <projectionBase>
            <vector x="-108.0" y="200.0" />
            <vector x="52.0" y="120.0" />
        </projectionBase>
    </diagram>
    <diagram title="GridScale_RULEncoded_x_Speed">
        <node id="0">
            <position x="425.5170288085937" y="159.49326070149735" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;0) AND (ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="1">
            <position x="52.0" y="120.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;0) AND (ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>ALLOY_SPEED_METER_MINUTE_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="2">
            <position x="1224.5510864257797" y="358.4797821044919" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="3">
            <position x="104.0" y="240.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>ALLOY_SPEED_METER_MINUTE_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="4">
            <position x="1120.5510864257797" y="118.47978210449236" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;2</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="5">
            <position x="747.034057617188" y="78.98652140299458" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;1</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="6">
            <position x="851.0340576171878" y="318.98652140299504" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="7">
            <position x="799.0340576171873" y="198.98652140299555" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;1) AND (RUL_CLASS_ENCODED&lt;=2)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;0) AND (ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>2.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="8">
            <position x="0.0" y="0.0" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&lt;=0)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>0.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <node id="9">
            <position x="1172.55108642578" y="238.47978210449264" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;2)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;0) AND (ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>3.0</coordinate>
                <coordinate>1.0</coordinate>
            </ndimVector>
        </node>
        <node id="10">
            <position x="477.5170288085938" y="279.4932607014975" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&gt;1))</object>
                </objectContingent>
                <attributeContingent />
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>2.0</coordinate>
            </ndimVector>
        </node>
        <node id="11">
            <position x="373.5170288085936" y="39.49326070149746" />
            <attributeLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </attributeLabelStyle>
            <objectLabelStyle>
                <offset x="0.0" y="0.0" />
                <backgroundColor>#ffffffff</backgroundColor>
                <textColor>#ff000000</textColor>
                <textAlignment>left</textAlignment>
            </objectLabelStyle>
            <concept>
                <objectContingent>
                    <object>((RUL_CLASS_ENCODED&gt;0) AND (RUL_CLASS_ENCODED&lt;=1)) AND ((ALLOY_SPEED_METER_MINUTE_ENCODED&lt;=0))</object>
                </objectContingent>
                <attributeContingent>
                    <attribute>RUL_CLASS_ENCODED &gt;0</attribute>
                </attributeContingent>
            </concept>
            <ndimVector>
                <coordinate>1.0</coordinate>
                <coordinate>0.0</coordinate>
            </ndimVector>
        </node>
        <edge from="1" to="0" />
        <edge from="11" to="0" />
        <edge from="8" to="1" />
        <edge from="9" to="2" />
        <edge from="6" to="2" />
        <edge from="1" to="3" />
        <edge from="5" to="4" />
        <edge from="11" to="5" />
        <edge from="7" to="6" />
        <edge from="10" to="6" />
        <edge from="0" to="7" />
        <edge from="5" to="7" />
        <edge from="4" to="9" />
        <edge from="7" to="9" />
        <edge from="0" to="10" />
        <edge from="3" to="10" />
        <edge from="8" to="11" />
        <projectionBase>
            <vector x="-108.0" y="200.0" />
            <vector x="52.0" y="120.0" />
        </projectionBase>
    </diagram>
</conceptualSchema>

