/*=======================================
 shape_test.cpp:                k-vernooy
 last modified:                Sun, Feb 9
 
 A driver program for testing methods in
 the shape classes (state, precinct, etc)
========================================*/

// #include "../include/shape.hpp"
#include "../include/geometry.hpp"
#include "../include/canvas.hpp"
// #include "../include/term_disp.hpp"

using namespace std;
// using namespace Geometry;

// void assert_equal(string context, float n1, float n2) {
//     if ( n1 != n2 )
//         cout << RED << "error " << RESET << "in " << context << ", " << n1 << " != " << n2;
//     else
//         cout << GREEN << "passed " << RESET << context << ", " << n1 << " = " << n2;
//     cout << endl;
// }

int main(int argc, char* argv[]) {

    Graphics::Color green(17, 255, 0);
    Graphics::Color blue(0, 17, 255);
    Geometry::LinearRing t({{-79645461, 41998859},{-79678786, 41999338},{-79694765, 41998856},{-79761313, 41998808},{-79761620, 42000060},{-79761709, 42118820},{-79762073, 42129489},{-79761732, 42155302},{-79762144, 42243166},{-79761832, 42243303},{-79762569, 42375058},{-79762418, 42516072},{-79476942, 42625057},{-79143474, 42750057},{-79124764, 42757423},{-78999760, 42804368},{-78930559, 42850105},{-78905758, 42899957},{-78905659, 42923357},{-78909159, 42933257},{-78918859, 42946857},{-78932360, 42955857},{-78961761, 42957756},{-78975062, 42968756},{-79011563, 42985256},{-79019964, 42994756},{-79023256, 43016356},{-79011747, 43028956},{-79005139, 43047056},{-78999435, 43056057},{-79007130, 43065757},{-79074459, 43077863},{-79075367, 43081355},{-79067333, 43089947},{-79065961, 43091052},{-79057961, 43106957},{-79058262, 43109279},{-79059267, 43112155},{-79060200, 43113604},{-79061957, 43115362},{-79069556, 43120255},{-79059660, 43126248},{-79056767, 43126855},{-79053772, 43129730},{-79049460, 43135050},{-79044057, 43138049},{-79042357, 43143654},{-79042931, 43149643},{-79044413, 43152603},{-79046538, 43162320},{-79048456, 43164655},{-79052925, 43173460},{-79052567, 43183655},{-79048658, 43199655},{-79057058, 43210654},{-79052858, 43222055},{-79055858, 43238554},{-79056060, 43254156},{-79070452, 43262455},{-79200936, 43450422},{-79124770, 43478464},{-79063719, 43500020},{-78998166, 43522500},{-78749761, 43609258},{-78711567, 43625413},{-78688295, 43634742},{-78624745, 43634799},{-78499752, 43633519},{-78374749, 43633178},{-78374749, 43632092},{-78124742, 43631175},{-77874735, 43631471},{-77696302, 43631262},{-77499725, 43632084},{-77374797, 43631475},{-77249715, 43631540},{-77249715, 43630594},{-77124710, 43631118},{-76999734, 43629204},{-76776233, 43629529},{-76753538, 43684275},{-76701286, 43750059},{-76624682, 43845569},{-76600108, 43875041},{-76499670, 43999538},{-76498927, 44000059},{-76438287, 44094172},{-76374672, 44123889},{-76352679, 44134743},{-76312639, 44199045},{-76286546, 44203767},{-76249661, 44204165},{-76245487, 44203664},{-76206774, 44214538},{-76191324, 44221239},{-76164258, 44239603},{-76161825, 44280776},{-76130884, 44296635},{-76129198, 44295170},{-76118136, 44294850},{-76111931, 44298031},{-76097351, 44299541},{-76045224, 44331720},{-76008361, 44343856},{-76000998, 44347534},{-75991537, 44347399},{-75991437, 44347124},{-75982394, 44347401},{-75979810, 44346193},{-75978598, 44346349},{-75978276, 44346873},{-75974833, 44346163},{-75973059, 44343626},{-75971753, 44342965},{-75970178, 44342828},{-75949540, 44349129},{-75939664, 44355395},{-75929465, 44359603},{-75921719, 44368886},{-75912985, 44368084},{-75871496, 44394839},{-75820819, 44432239},{-75807765, 44471641},{-75766226, 44515847},{-75749677, 44526950},{-75727052, 44542812},{-75696583, 44567581},{-75662373, 44591927},{-75650953, 44599363},{-75618364, 44619637},{-75580913, 44648522},{-75505902, 44705081},{-75477641, 44720224},{-75423938, 44756327},{-75413792, 44772534},{-75397013, 44773467},{-75387367, 44780026},{-75374680, 44782318},{-75369953, 44782883},{-75369829, 44788065},{-75344538, 44809139},{-75333743, 44806375},{-75301976, 44826637},{-75307621, 44836810},{-75283128, 44849148},{-75270604, 44854034},{-75262594, 44856327},{-75255516, 44857655},{-75241294, 44866948},{-75228638, 44867891},{-75218576, 44877569},{-75203012, 44877548},{-75194072, 44882625},{-75188277, 44883212},{-75165123, 44893324},{-75139866, 44896684},{-75134416, 44915102},{-75124657, 44918427},{-75117575, 44921342},{-75105086, 44919541},{-75096659, 44927067},{-75064826, 44929449},{-75059966, 44934570},{-75027125, 44946568},{-75005151, 44958406},{-75003083, 44962412},{-74999878, 44965911},{-74999258, 44966111},{-74999270, 44971638},{-74992727, 44977469},{-74972418, 44983414},{-74947506, 44984583},{-74907948, 44983369},{-74900725, 44992761},{-74888042, 44999658},{-74887837, 45000046},{-74877232, 45001362},{-74866640, 45000536},{-74862643, 45004591},{-74856422, 45004524},{-74846175, 45010290},{-74841790, 45011415},{-74834674, 45014698},{-74826576, 45015865},{-74817195, 45011728},{-74813263, 45013543},{-74801638, 45014569},{-74799885, 45010707},{-74793149, 45004645},{-74763407, 45005613},{-74760217, 44994945},{-74744640, 44990562},{-74731301, 44990419},{-74722573, 44998064},{-74702019, 45003322},{-74686932, 45000098},{-74683966, 44999690},{-74678402, 45000048},{-74673047, 45000943},{-74670297, 45006194},{-74661479, 44999593},{-74624632, 44999513},{-74624632, 44999280},{-74549020, 44998699},{-74457530, 44997033},{-74410329, 44995403},{-74404432, 44994921},{-74374639, 44993854},{-74335184, 44991905},{-74308242, 44992183},{-74234136, 44992148},{-74205034, 44991791},{-74193031, 44991987},{-74150235, 44991357},{-73874597, 45001223},{-73792278, 45002998},{-73762986, 45003239},{-73675459, 45002907},{-73639718, 45003464},{-73437372, 45009198},{-73343124, 45010840},{-73350188, 44994304},{-73350862, 44993049},{-73353429, 44990165},{-73354633, 44987352},{-73354112, 44984062},{-73352886, 44980644},{-73350218, 44976222},{-73347579, 44973038},{-73344740, 44970468},{-73338735, 44965887},{-73338244, 44964751},{-73337907, 44960542},{-73339030, 44951338},{-73339603, 44943371},{-73338483, 44924112},{-73338622, 44919366},{-73338979, 44917681},{-73339439, 44916534},{-73341106, 44914632},{-73350652, 44909634},{-73353657, 44907346},{-73356218, 44904492},{-73360328, 44897236},{-73362230, 44891463},{-73366460, 44875041},{-73369104, 44866681},{-73371968, 44862415},{-73375709, 44860746},{-73376331, 44860238},{-73377482, 44858151},{-73379822, 44857038},{-73379877, 44855540},{-73379365, 44852553},{-73379545, 44851651},{-73379986, 44850837},{-73381590, 44849354},{-73380321, 44847173},{-73381336, 44844683},{-73379684, 44843904},{-73379447, 44843461},{-73379918, 44840578},{-73379452, 44838010},{-73378717, 44837358},{-73375346, 44836307},{-73372686, 44832997},{-73371330, 44830742},{-73368275, 44828007},{-73365679, 44826451},{-73358081, 44823310},{-73353472, 44820386},{-73350200, 44816394},{-73345080, 44813015},{-73340906, 44808356},{-73335044, 44804109},{-73334430, 44802189},{-73333750, 44797880},{-73333154, 44788759},{-73333771, 44785192},{-73335713, 44782086},{-73339958, 44778893},{-73344261, 44776280},{-73347085, 44772980},{-73348712, 44768230},{-73350019, 44765279},{-73351193, 44763647},{-73352382, 44759521},{-73354361, 44755296},{-73357671, 44751018},{-73361497, 44747772},{-73363792, 44745254},{-73365562, 44741786},{-73365723, 44739846},{-73365084, 44733830},{-73365069, 44725647},{-73365547, 44719202},{-73365247, 44710648},{-73365784, 44707095},{-73365326, 44703294},{-73365977, 44697559},{-73365249, 44696570},{-73361744, 44695820},{-73361323, 44695370},{-73361308, 44694524},{-73362316, 44692492},{-73364371, 44689878},{-73364726, 44688435},{-73365297, 44687548},{-73370142, 44684855},{-73369685, 44683760},{-73367414, 44681293},{-73367209, 44678514},{-73367546, 44678151},{-73371089, 44677531},{-73371843, 44676957},{-73371872, 44675934},{-73371010, 44672763},{-73372719, 44668739},{-73372547, 44668184},{-73370064, 44666071},{-73369668, 44663478},{-73370071, 44662753},{-73370589, 44662518},{-73373062, 44662713},{-73374577, 44661890},{-73377209, 44658142},{-73379073, 44656772},{-73378967, 44655180},{-73378013, 44653846},{-73377972, 44652918},{-73378317, 44652165},{-73381148, 44649002},{-73383974, 44647605},{-73384483, 44646683},{-73383564, 44646142},{-73378560, 44641476},{-73379747, 44640361},{-73385811, 44637202},{-73386783, 44636370},{-73387169, 44635543},{-73385899, 44631044},{-73386497, 44626925},{-73387346, 44623673},{-73389966, 44619621},{-73390231, 44618354},{-73389820, 44617211},{-73382932, 44612184},{-73382393, 44611346},{-73381619, 44607221},{-73380725, 44605240},{-73379576, 44603063},{-73376849, 44599599},{-73376332, 44597219},{-73376806, 44595456},{-73377897, 44593849},{-73381640, 44590583},{-73381849, 44589316},{-73377795, 44585128},{-73375667, 44582038},{-73375230, 44580204},{-73375308, 44577546},{-73374950, 44575817},{-73370301, 44572013},{-73367343, 44567605},{-73360088, 44562547},{-73356789, 44557919},{-73355187, 44556919},{-73350822, 44555790},{-73344001, 44552509},{-73342384, 44551449},{-73338752, 44548046},{-73338609, 44546132},{-73339307, 44544477},{-73339006, 44543301},{-73331608, 44535920},{-73330910, 44534269},{-73330603, 44531033},{-73329746, 44529565},{-73328522, 44528469},{-73323941, 44527113},{-73322039, 44525286},{-73321702, 44524395},{-73321823, 44521903},{-73321121, 44519857},{-73321428, 44516256},{-73320846, 44513630},{-73319270, 44511955},{-73316662, 44510372},{-73312874, 44507244},{-73308603, 44502767},{-73306713, 44500335},{-73304982, 44492590},{-73304429, 44485739},{-73304107, 44484585},{-73300658, 44478559},{-73299896, 44476651},{-73299161, 44472910},{-73298706, 44469617},{-73298706, 44464453},{-73300170, 44455805},{-73300125, 44454711},{-73299480, 44453009},{-73295225, 44445883},{-73293870, 44442149},{-73293627, 44438903},{-73296052, 44428334},{-73309599, 44404505},{-73310505, 44402601},{-73312441, 44394706},{-73315040, 44388526},{-73317066, 44385991},{-73320981, 44382685},{-73330396, 44376000},{-73333613, 44372300},{-73334950, 44364440},{-73334648, 44356879},{-73330255, 44349824},{-73327353, 44344360},{-73325150, 44338528},{-73324021, 44333835},{-73323828, 44325165},{-73324526, 44319246},{-73324195, 44310033},{-73322216, 44301542},{-73320124, 44295909},{-73316767, 44287728},{-73312210, 44280069},{-73310914, 44274298},{-73312741, 44265411},{-73316427, 44257737},{-73319603, 44249909},{-73322479, 44248733},{-73323067, 44247896},{-73323364, 44246910},{-73323174, 44245061},{-73323715, 44244160},{-73324653, 44243517},{-73330375, 44244312},{-73336403, 44239781},{-73339119, 44238893},{-73343376, 44238190},{-73343567, 44237220},{-73342636, 44235334},{-73342835, 44234446},{-73349510, 44230905},{-73350479, 44229893},{-73351379, 44225980},{-73355377, 44223157},{-73355690, 44222072},{-73355660, 44220055},{-73356224, 44218956},{-73357826, 44217331},{-73358902, 44215474},{-73361640, 44213354},{-73362220, 44212461},{-73361847, 44209421},{-73362266, 44208518},{-73363393, 44207737},{-73368660, 44205729},{-73370865, 44204527},{-73373739, 44200964},{-73374802, 44200243},{-73377876, 44199567},{-73381935, 44197734},{-73383392, 44195936},{-73383759, 44194032},{-73384582, 44193193},{-73385925, 44192766},{-73388893, 44192619},{-73390022, 44191888},{-73390625, 44191068},{-73390907, 44188110},{-73389824, 44181757},{-73390228, 44180331},{-73390876, 44179350},{-73391907, 44178428},{-73394653, 44177377},{-73396065, 44175776},{-73397171, 44173838},{-73397492, 44170912},{-73396007, 44168232},{-73395813, 44166266},{-73396759, 44164514},{-73397614, 44163797},{-73398857, 44161915},{-73400291, 44154363},{-73400933, 44152698},{-73402397, 44151539},{-73402877, 44150483},{-73402146, 44148060},{-73402214, 44146944},{-73403045, 44144984},{-73408127, 44139897},{-73411972, 44137780},{-73415649, 44133451},{-73416138, 44132355},{-73414162, 44128159},{-73414049, 44124082},{-73412496, 44121275},{-73412027, 44119631},{-73411225, 44113767},{-73411512, 44111952},{-73412044, 44110641},{-73413933, 44107845},{-73415215, 44101344},{-73418579, 44096637},{-73429215, 44079831},{-73429718, 44078586},{-73430038, 44077195},{-73430234, 44071941},{-73431122, 44067766},{-73434654, 44055300},{-73437210, 44048438},{-73437905, 44045125},{-73437500, 44043460},{-73436729, 44042633},{-73426899, 44036692},{-73425090, 44034376},{-73422882, 44032548},{-73415347, 44029869},{-73412512, 44028346},{-73410385, 44026503},{-73407645, 44021111},{-73405899, 44015341},{-73406009, 44011417},{-73407544, 44004363},{-73408805, 44000679},{-73409057, 43996012},{-73410408, 43991851},{-73411177, 43986292},{-73412048, 43984388},{-73412510, 43982216},{-73412048, 43977604},{-73407069, 43968172},{-73406469, 43962972},{-73406448, 43959582},{-73405736, 43955932},{-73405646, 43948069},{-73407448, 43942480},{-73408554, 43937310},{-73408859, 43934505},{-73408554, 43931894},{-73407134, 43928186},{-73402364, 43919906},{-73396179, 43903264},{-73383694, 43891284},{-73374162, 43876241},{-73374344, 43874308},{-73376554, 43869607},{-73379355, 43864643},{-73379697, 43863170},{-73381248, 43860018},{-73382309, 43856058},{-73382004, 43854113},{-73380249, 43851923},{-73373627, 43847521},{-73372841, 43846636},{-73372589, 43845354},{-73373711, 43842966},{-73376663, 43839434},{-73383095, 43836482},{-73386261, 43834424},{-73388192, 43832655},{-73389297, 43831235},{-73392250, 43824829},{-73392799, 43822771},{-73392517, 43821340},{-73391014, 43818411},{-73389565, 43817040},{-73385666, 43814806},{-73382057, 43812216},{-73380722, 43810819},{-73379601, 43809201},{-73378196, 43805930},{-73376793, 43799158},{-73370995, 43795132},{-73364059, 43791215},{-73358154, 43786475},{-73357521, 43785557},{-73355362, 43777927},{-73354401, 43776373},{-73350998, 43772434},{-73350762, 43771387},{-73351265, 43769823},{-73354644, 43764564},{-73362823, 43753084},{-73365259, 43750004},{-73365944, 43749738},{-73366883, 43747661},{-73369944, 43743855},{-73370331, 43742230},{-73370724, 43735570},{-73370241, 43733448},{-73369916, 43728789},{-73370612, 43725329},{-73377756, 43717713},{-73382965, 43714059},{-73385883, 43711337},{-73388167, 43708509},{-73388762, 43706405},{-73389807, 43705721},{-73392760, 43702038},{-73393723, 43699200},{-73395517, 43696831},{-73398332, 43694625},{-73402195, 43693011},{-73403290, 43692132},{-73404739, 43690214},{-73405243, 43688368},{-73403926, 43686220},{-73403475, 43684695},{-73404127, 43681340},{-73407777, 43672519},{-73408062, 43669438},{-73412108, 43661659},{-73414546, 43658209},{-73415093, 43656710},{-73415189, 43653467},{-73415513, 43652451},{-73418574, 43648051},{-73424027, 43645403},{-73426463, 43642599},{-73426955, 43640526},{-73428583, 43636543},{-73428419, 43635453},{-73426914, 43633144},{-73418320, 43623325},{-73417669, 43621687},{-73417828, 43620586},{-73423709, 43612357},{-73423816, 43610990},{-73422155, 43606512},{-73421616, 43603023},{-73422421, 43601557},{-73424977, 43598775},{-73426882, 43595215},{-73430325, 43590532},{-73431229, 43588285},{-73430948, 43587036},{-73428637, 43583994},{-73426664, 43582975},{-73422159, 43582130},{-73420379, 43581490},{-73416965, 43577731},{-73403911, 43570331},{-73403052, 43570223},{-73402151, 43569546},{-73398126, 43568065},{-73395768, 43568087},{-73395169, 43569619},{-73393120, 43569601},{-73391673, 43570120},{-73391344, 43570851},{-73391891, 43572949},{-73390794, 43574183},{-73389741, 43574683},{-73387311, 43574668},{-73384935, 43575114},{-73384339, 43575398},{-73383285, 43577200},{-73382711, 43579196},{-73383414, 43580550},{-73384897, 43582055},{-73385251, 43583263},{-73382616, 43585625},{-73382465, 43586578},{-73382930, 43587076},{-73384320, 43587334},{-73386253, 43588411},{-73387039, 43589463},{-73386901, 43590770},{-73385833, 43591426},{-73383518, 43591308},{-73382138, 43591824},{-73381715, 43592963},{-73383540, 43596800},{-73383490, 43597366},{-73381601, 43598488},{-73380271, 43597905},{-73377370, 43598398},{-73377194, 43598815},{-73377748, 43599656},{-73377636, 43600228},{-73373443, 43603292},{-73372469, 43604848},{-73372375, 43606014},{-73373163, 43607248},{-73374066, 43607979},{-73376386, 43608824},{-73376039, 43609304},{-73374226, 43610197},{-73374242, 43610860},{-73376037, 43612117},{-73375595, 43613351},{-73369840, 43619392},{-73372487, 43622752},{-73372456, 43623666},{-73371890, 43624490},{-73371104, 43624756},{-73368900, 43624711},{-73368271, 43624586},{-73367168, 43623623},{-73365563, 43623441},{-73359111, 43624599},{-73358455, 43625416},{-73357291, 43625906},{-73354270, 43626190},{-73353638, 43625927},{-73352610, 43624085},{-73351232, 43622502},{-73349985, 43621633},{-73348753, 43621458},{-73347621, 43622510},{-73346992, 43624156},{-73344510, 43626277},{-73342842, 43626506},{-73342181, 43626071},{-73341578, 43624739},{-73340068, 43624647},{-73338026, 43625442},{-73337806, 43626095},{-73337365, 43626324},{-73334218, 43626919},{-73334187, 43627994},{-73333683, 43628017},{-73332078, 43627171},{-73331290, 43626074},{-73327702, 43625914},{-73325939, 43626463},{-73324492, 43627515},{-73319928, 43627333},{-73318322, 43628499},{-73317850, 43628499},{-73317315, 43627081},{-73313129, 43625512},{-73312967, 43624706},{-73311173, 43624092},{-73310229, 43624229},{-73307471, 43628000},{-73306440, 43628333},{-73304126, 43627058},{-73302553, 43625709},{-73302077, 43624365},{-73302076, 43623108},{-73302990, 43620524},{-73302455, 43619632},{-73300378, 43617803},{-73300315, 43617323},{-73301134, 43616019},{-73300851, 43613458},{-73302236, 43611789},{-73302772, 43609777},{-73302111, 43609388},{-73301607, 43609503},{-73300883, 43610737},{-73300285, 43610806},{-73299876, 43610394},{-73298020, 43610028},{-73297863, 43609434},{-73296699, 43608633},{-73296416, 43607604},{-73295283, 43606849},{-73295000, 43606049},{-73293742, 43605203},{-73293711, 43604357},{-73292216, 43602555},{-73292698, 43601955},{-73292646, 43601340},{-73292158, 43600567},{-73291161, 43599878},{-73291019, 43599235},{-73292679, 43597088},{-73292358, 43595752},{-73293280, 43592547},{-73296944, 43587314},{-73294189, 43585777},{-73292363, 43585137},{-73292109, 43584544},{-73297324, 43579373},{-73295668, 43578633},{-73295725, 43577146},{-73295292, 43576782},{-73294506, 43577148},{-73294285, 43577788},{-73294474, 43578314},{-73294128, 43578474},{-73292021, 43578588},{-73291109, 43577856},{-73290040, 43577673},{-73289159, 43578336},{-73284912, 43579272},{-73283592, 43578083},{-73282051, 43578128},{-73281296, 43577579},{-73280858, 43573578},{-73280292, 43573555},{-73279726, 43574241},{-73278751, 43574057},{-73277807, 43574629},{-73276549, 43574468},{-73276319, 43573410},{-73273753, 43572657},{-73271663, 43572433},{-73269700, 43571770},{-73267932, 43572250},{-73267532, 43571811},{-73268452, 43571434},{-73267458, 43570873},{-73268347, 43570448},{-73269290, 43570506},{-73268988, 43569929},{-73268269, 43569669},{-73267539, 43569981},{-73267936, 43569137},{-73267528, 43569000},{-73266679, 43569160},{-73266489, 43569868},{-73264163, 43569136},{-73264602, 43568195},{-73264008, 43567592},{-73263097, 43567674},{-73262358, 43567278},{-73261899, 43566143},{-73262078, 43565701},{-73261149, 43565788},{-73260739, 43566535},{-73258631, 43564950},{-73258192, 43564287},{-73258350, 43563052},{-73255930, 43561885},{-73255555, 43559895},{-73253827, 43558431},{-73252602, 43556852},{-73252603, 43556441},{-73254395, 43556282},{-73254490, 43555596},{-73251441, 43555388},{-73248641, 43553858},{-73248766, 43553149},{-73248420, 43552578},{-73248985, 43552417},{-73249160, 43551754},{-73248607, 43551206},{-73250219, 43550792},{-73250408, 43550426},{-73249965, 43549374},{-73249206, 43548896},{-73249269, 43548461},{-73250028, 43547933},{-73250029, 43547522},{-73249253, 43547204},{-73249189, 43546655},{-73249856, 43546127},{-73248193, 43545787},{-73247815, 43545055},{-73249157, 43545283},{-73249936, 43544869},{-73250133, 43543429},{-73249554, 43543064},{-73247813, 43542814},{-73246586, 43541855},{-73246710, 43540346},{-73246395, 43539751},{-73244414, 43538815},{-73243531, 43535408},{-73242839, 43534768},{-73241587, 43534969},{-73241717, 43534399},{-73242537, 43534381},{-73242744, 43533991},{-73241391, 43532346},{-73242647, 43530722},{-73242678, 43530105},{-73241892, 43529419},{-73243367, 43527727},{-73245440, 43526857},{-73246821, 43525781},{-73246820, 43524615},{-73247698, 43523174},{-73246502, 43521460},{-73247601, 43520522},{-73247631, 43519241},{-73246720, 43518876},{-73246844, 43517252},{-73248037, 43516360},{-73248068, 43515994},{-73246716, 43515332},{-73247061, 43514920},{-73248396, 43470634},{-73252258, 43375072},{-73252833, 43363494},{-73253303, 43361208},{-73253085, 43354714},{-73256475, 43260093},{-73258697, 43230555},{-73259159, 43216848},{-73265595, 43095926},{-73269777, 43035976},{-73274170, 42949028},{-73275961, 42901225},{-73275804, 42897249},{-73278306, 42837558},{-73278673, 42833410},{-73284311, 42834954},{-73285388, 42834093},{-73287063, 42820140},{-73283695, 42813856},{-73286547, 42809484},{-73286343, 42808063},{-73290944, 42801920},{-73276421, 42746019},{-73264957, 42745940},{-73356031, 42500018},{-73356894, 42498360},{-73362064, 42483235},{-73362768, 42481955},{-73450974, 42242779},{-73508142, 42086257},{-73496879, 42049675},{-73487314, 42049638},{-73489615, 42000092},{-73492988, 41958287},{-73496599, 41921797},{-73498304, 41892509},{-73501984, 41858717},{-73505315, 41823928},{-73505245, 41821822},{-73510961, 41758749},{-73511921, 41740941},{-73516785, 41687581},{-73520017, 41641197},{-73521041, 41619773},{-73525994, 41572120},{-73527692, 41549951},{-73529313, 41535629},{-73532504, 41500061},{-73535568, 41460524},{-73536334, 41446632},{-73537888, 41431885},{-73541469, 41404394},{-73543425, 41376622},{-73545121, 41363294},{-73549088, 41325134},{-73549879, 41301522},{-73550962, 41295421},{-73512948, 41250095},{-73482695, 41212772},{-73488412, 41210006},{-73513993, 41198854},{-73535996, 41188435},{-73591828, 41163002},{-73597001, 41160888},{-73600190, 41159149},{-73651673, 41136096},{-73727775, 41100696},{-73723382, 41094437},{-73718675, 41089996},{-73705073, 41072495},{-73682473, 41044697},{-73679275, 41041384},{-73671074, 41031527},{-73670377, 41030059},{-73662756, 41020573},{-73658992, 41017178},{-73655255, 41012246},{-73656065, 41008923},{-73660268, 41000484},{-73659309, 40997171},{-73659585, 40994140},{-73657228, 40990914},{-73659671, 40987909},{-73656771, 40984509},{-73612885, 40950943},{-73374560, 41001060},{-73275392, 41021120},{-73249557, 41025866},{-73229104, 41030604},{-73183476, 41042052},{-72999547, 41087108},{-72803115, 41125097},{-72527901, 41177774},{-72249553, 41230526},{-72141534, 41250098},{-72081847, 41262224},{-72019214, 41290594},{-71999486, 41295794},{-71929451, 41310387},{-71907258, 41304483},{-71879847, 41276246},{-71858513, 41253697},{-71854462, 41250100},{-71790972, 41184101},{-71790635, 41101837},{-71781872, 41096197},{-71779244, 41088442},{-71777491, 41077162},{-71777491, 41067292},{-71782748, 41055307},{-71794139, 41036977},{-71808163, 41027812},{-71837088, 41010892},{-71864619, 41000102},{-71870139, 40996971},{-71876434, 40994719},{-71884775, 40992269},{-71896835, 40990625},{-71899907, 40990496},{-71927470, 40983308},{-71931698, 40982497},{-71970135, 40967746},{-71999516, 40956019},{-72249525, 40866765},{-72374529, 40818595},{-72396531, 40812603},{-72624539, 40745567},{-72749544, 40713405},{-72828607, 40686901},{-72874542, 40675019},{-73014004, 40625099},{-73032084, 40619528},{-73064093, 40611667},{-73085149, 40607013},{-73095301, 40605273},{-73124558, 40598366},{-73249642, 40562565},{-73274025, 40551314},{-73291441, 40551314},{-73312340, 40554115},{-73326272, 40556916},{-73343688, 40554116},{-73378519, 40545713},{-73406384, 40537310},{-73441215, 40531709},{-73465597, 40526107},{-73486496, 40520505},{-73517844, 40523306},{-73552674, 40528909},{-73624574, 40534511},{-73706094, 40534542},{-73768781, 40533747},{-73783969, 40532387},{-73826158, 40522874},{-73854843, 40512000},{-73870029, 40502486},{-73876778, 40501127},{-73882272, 40495210},{-73886652, 40489794},{-73949912, 40525540},{-74057595, 40506529},{-74094483, 40499601},{-74228153, 40477399},{-74253313, 40487386},{-74259090, 40497207},{-74259089, 40502890},{-74258291, 40507905},{-74254810, 40515344},{-74246069, 40520952},{-74246444, 40524673},{-74248787, 40533033},{-74250609, 40541851},{-74247415, 40549200},{-74239211, 40553764},{-74231693, 40558457},{-74218398, 40556996},{-74215278, 40560241},{-74208968, 40576563},{-74206298, 40588542},{-74203688, 40592691},{-74199520, 40597539},{-74199408, 40600201},{-74203813, 40605961},{-74203128, 40614109},{-74201864, 40618557},{-74203737, 40624227},{-74202441, 40628521},{-74202247, 40630903},{-74196990, 40635832},{-74195664, 40637648},{-74189680, 40643188},{-74185636, 40645995},{-74181390, 40646475},{-74143255, 40642149},{-74133912, 40643684},{-74125569, 40644023},{-74109976, 40648011},{-74093746, 40648239},{-74086806, 40651596},{-74055739, 40651760},{-74026284, 40699902},{-74021117, 40727417},{-74013784, 40756601},{-74009184, 40763601},{-73997383, 40780301},{-73974882, 40810800},{-73968081, 40820701},{-73963182, 40826900},{-73953982, 40848000},{-73948385, 40858471},{-73929821, 40888682},{-73920967, 40911012},{-73919097, 40914806},{-73918405, 40917477},{-73917905, 40917577},{-73917681, 40919499},{-73915581, 40924898},{-73907280, 40951498},{-73896479, 40981701},{-73893979, 40997205},{-73902679, 40997307},{-73905010, 40997591},{-73911880, 41001297},{-73920155, 41005186},{-73964782, 41025297},{-74042784, 41059796},{-74045885, 41061397},{-74061365, 41067901},{-74071915, 41072883},{-74127188, 41097096},{-74142288, 41104195},{-74182390, 41121595},{-74206791, 41131295},{-74232992, 41142195},{-74249592, 41149795},{-74301994, 41172594},{-74320909, 41182353},{-74378843, 41208967},{-74457584, 41248225},{-74499603, 41267344},{-74607348, 41317774},{-74641599, 41332905},{-74694694, 41357360},{-74696398, 41357339},{-74691072, 41360339},{-74689756, 41361559},{-74689502, 41363851},{-74691115, 41367343},{-74694960, 41370431},{-74703283, 41375094},{-74708459, 41378902},{-74710392, 41382103},{-74713412, 41389814},{-74715980, 41392584},{-74720892, 41394690},{-74726952, 41395102},{-74730385, 41395660},{-74733640, 41396975},{-74736103, 41398398},{-74738554, 41401191},{-74740963, 41405120},{-74741717, 41407880},{-74741569, 41409925},{-74741083, 41411415},{-74738685, 41413463},{-74736922, 41416975},{-74734732, 41422700},{-74734894, 41425819},{-74735520, 41427466},{-74736689, 41429229},{-74738456, 41430642},{-74740933, 41431161},{-74743822, 41430636},{-74750680, 41427985},{-74754359, 41425148},{-74756335, 41424044},{-74758587, 41423287},{-74760826, 41423215},{-74763701, 41423613},{-74766703, 41424452},{-74770650, 41426230},{-74773239, 41426352},{-74778029, 41425104},{-74784339, 41422397},{-74787517, 41421763},{-74790417, 41421660},{-74793856, 41422671},{-74795396, 41423980},{-74796499, 41425393},{-74799546, 41431290},{-74800095, 41432661},{-74800370, 41436060},{-74801225, 41438100},{-74805655, 41442101},{-74807582, 41442847},{-74812123, 41442982},{-74817995, 41440505},{-74822880, 41436792},{-74826031, 41431736},{-74828592, 41430698},{-74830671, 41430503},{-74834636, 41430795},{-74836915, 41431625},{-74845572, 41437577},{-74848602, 41440179},{-74854200, 41443166},{-74858578, 41444427},{-74864688, 41443993},{-74871421, 41441781},{-74874333, 41441281},{-74876721, 41440338},{-74880174, 41439648},{-74889642, 41438159},{-74892625, 41438617},{-74894838, 41439265},{-74896025, 41439987},{-74896399, 41442179},{-74894931, 41446099},{-74893400, 41447742},{-74889704, 41450299},{-74889075, 41451245},{-74889116, 41452534},{-74890358, 41455324},{-74890915, 41456180},{-74892114, 41456959},{-74895069, 41458190},{-74904194, 41459805},{-74906887, 41461131},{-74908103, 41464639},{-74908133, 41468117},{-74909181, 41472436},{-74910606, 41474174},{-74912991, 41475901},{-74917281, 41477044},{-74922173, 41476855},{-74924092, 41477138},{-74926835, 41478327},{-74932585, 41482323},{-74934652, 41482872},{-74941798, 41483542},{-74944756, 41483491},{-74945634, 41483213},{-74948080, 41480625},{-74956411, 41476735},{-74958260, 41476396},{-74968278, 41477166},{-74982513, 41480319},{-74983341, 41480894},{-74984259, 41482210},{-74985595, 41485863},{-74985247, 41489113},{-74982463, 41496467},{-74982168, 41498486},{-74982385, 41500981},{-74984372, 41506611},{-74985626, 41507904},{-74987645, 41508738},{-74993893, 41508754},{-74999614, 41507400},{-75001210, 41507441},{-75003151, 41508101},{-75003682, 41509269},{-75003706, 41511118},{-75002592, 41514560},{-75000982, 41517508},{-75000911, 41519292},{-75001297, 41520650},{-75003850, 41524052},{-75009552, 41528461},{-75014919, 41531399},{-75016616, 41532110},{-75023018, 41533147},{-75024206, 41534018},{-75024757, 41535099},{-75025064, 41538418},{-75024798, 41539801},{-75022838, 41541453},{-75017626, 41542734},{-75016144, 41544246},{-75015994, 41545103},{-75016328, 41546501},{-75018524, 41551802},{-75024550, 41559231},{-75027343, 41563541},{-75029211, 41564637},{-75031684, 41564644},{-75033165, 41565093},{-75036989, 41567049},{-75040490, 41569688},{-75043581, 41573873},{-75045651, 41580853},{-75046760, 41583258},{-75052858, 41587772},{-75057300, 41589414},{-75060012, 41590813},{-75063677, 41594739},{-75066955, 41599428},{-75069698, 41602002},{-75074613, 41605711},{-75074625, 41607905},{-75073807, 41608585},{-75071667, 41609501},{-75067795, 41610143},{-75062716, 41609639},{-75059725, 41610801},{-75059575, 41611198},{-75059956, 41612306},{-75061675, 41615468},{-75061560, 41616429},{-75060098, 41617482},{-75055681, 41618606},{-75053850, 41618655},{-75051856, 41618157},{-75048385, 41615986},{-75047298, 41615791},{-75045508, 41616203},{-75044741, 41616810},{-75044224, 41617978},{-75044332, 41621009},{-75043562, 41623640},{-75044632, 41625086},{-75046135, 41628456},{-75048199, 41632011},{-75048658, 41633781},{-75048684, 41638296},{-75049281, 41641862},{-75048812, 41643947},{-75047683, 41645356},{-75047712, 41645928},{-75049014, 41647806},{-75049115, 41648500},{-75048683, 41656317},{-75048871, 41658662},{-75049920, 41662556},{-75053991, 41668194},{-75054740, 41668631},{-75057251, 41668933},{-75058430, 41669653},{-75059088, 41670892},{-75059332, 41672320},{-75058765, 41674412},{-75052653, 41678436},{-75051285, 41679961},{-75051234, 41682439},{-75052076, 41684351},{-75052736, 41688393},{-75056741, 41695696},{-75059829, 41699716},{-75067278, 41705434},{-75067915, 41706143},{-75068830, 41708161},{-75068642, 41710146},{-75067580, 41711861},{-75066630, 41712588},{-75064422, 41712950},{-75061176, 41712935},{-75052226, 41711396},{-75050689, 41711969},{-75049862, 41713309},{-75049699, 41715093},{-75050242, 41716969},{-75051831, 41719921},{-75052001, 41722105},{-75054102, 41729886},{-75054818, 41735168},{-75052808, 41744725},{-75053227, 41751662},{-75053431, 41752538},{-75056447, 41756905},{-75057463, 41759372},{-75060372, 41764200},{-75060756, 41764639},{-75064901, 41766686},{-75068567, 41767298},{-75072664, 41768807},{-75075268, 41771221},{-75076997, 41771649},{-75092810, 41768361},{-75099975, 41768901},{-75101752, 41769513},{-75103492, 41771238},{-75104334, 41772693},{-75104640, 41774203},{-75104013, 41776580},{-75103548, 41782008},{-75102329, 41786503},{-75101463, 41787941},{-75100026, 41789653},{-75096912, 41791917},{-75092876, 41796386},{-75090073, 41797310},{-75088328, 41797534},{-75084009, 41796666},{-75081415, 41796483},{-75078270, 41797467},{-75076889, 41798509},{-75075726, 41799724},{-75074412, 41802191},{-75072176, 41808318},{-75071751, 41810161},{-75071751, 41811901},{-75072172, 41813732},{-75073087, 41814630},{-75074409, 41815088},{-75078063, 41815112},{-75079818, 41814815},{-75085789, 41811626},{-75089484, 41811576},{-75093537, 41813375},{-75097264, 41815854},{-75100024, 41818347},{-75101302, 41818964},{-75113334, 41822782},{-75114837, 41825670},{-75115147, 41827285},{-75114998, 41830300},{-75113441, 41836298},{-75113369, 41840698},{-75113734, 41842352},{-75114399, 41843583},{-75117103, 41845463},{-75120769, 41845881},{-75127913, 41844903},{-75130983, 41845145},{-75135168, 41848415},{-75138852, 41850742},{-75140241, 41852078},{-75140938, 41852173},{-75144778, 41851484},{-75151965, 41848841},{-75154829, 41848292},{-75157350, 41848462},{-75159638, 41849092},{-75162854, 41850582},{-75165785, 41853266},{-75168406, 41858146},{-75168857, 41860378},{-75168055, 41867043},{-75168502, 41868929},{-75169692, 41870942},{-75170565, 41871608},{-75172532, 41872239},{-75175626, 41872673},{-75176633, 41872371},{-75177670, 41871384},{-75179591, 41869175},{-75180497, 41865680},{-75182271, 41862198},{-75183937, 41860515},{-75185254, 41859930},{-75186993, 41860109},{-75188888, 41861264},{-75190203, 41862454},{-75191441, 41865063},{-75192649, 41866285},{-75194382, 41867287},{-75197836, 41868807},{-75202357, 41869268},{-75204002, 41869867},{-75209741, 41869250},{-75214970, 41867449},{-75216463, 41865822},{-75220125, 41860534},{-75222996, 41857765},{-75223734, 41857456},{-75226676, 41857735},{-75227787, 41858187},{-75229283, 41859411},{-75230698, 41859164},{-75231612, 41859459},{-75234565, 41861569},{-75238743, 41865699},{-75241134, 41867118},{-75243345, 41866877},{-75248045, 41863300},{-75251197, 41862040},{-75257825, 41862154},{-75260527, 41863800},{-75262802, 41866213},{-75263673, 41868105},{-75263972, 41869668},{-75263815, 41870757},{-75263249, 41871765},{-75261488, 41873277},{-75258439, 41875087},{-75257821, 41875921},{-75257564, 41877108},{-75258656, 41880100},{-75260623, 41883783},{-75263005, 41885109},{-75267789, 41885982},{-75271293, 41887358},{-75272581, 41893168},{-75272778, 41897112},{-75267773, 41901971},{-75267371, 41904488},{-75267562, 41907054},{-75269736, 41911363},{-75275368, 41919564},{-75276552, 41922208},{-75276501, 41926679},{-75277243, 41933598},{-75278385, 41935767},{-75279094, 41938917},{-75282559, 41940416},{-75284679, 41941954},{-75289383, 41942891},{-75290966, 41945039},{-75291754, 41947082},{-75291902, 41948686},{-75291430, 41952477},{-75292589, 41953897},{-75293713, 41954593},{-75295236, 41954798},{-75298580, 41954524},{-75300409, 41953871},{-75301593, 41952811},{-75301738, 41951657},{-75301233, 41948900},{-75303010, 41948286},{-75303966, 41948216},{-75307519, 41949198},{-75310358, 41949012},{-75312817, 41950182},{-75318168, 41954236},{-75318701, 41957105},{-75320040, 41960867},{-75322384, 41961693},{-75326002, 41964751},{-75327859, 41967370},{-75328981, 41968420},{-75335841, 41970527},{-75339488, 41970786},{-75342204, 41972872},{-75342460, 41974303},{-75340448, 41977492},{-75339623, 41980930},{-75337791, 41984386},{-75337602, 41986700},{-75341125, 41992772},{-75346568, 41995324},{-75353504, 41997110},{-75359579, 41999445},{-75610316, 41998959},{-75761136, 41997790},{-75870677, 41998828},{-75888502, 41998892},{-75890619, 41998606},{-75980250, 41999035},{-76090973, 41998779},{-76128575, 41999023},{-76149603, 41998635},{-76346950, 41998320},{-76445259, 41998707},{-76533056, 41999923},{-76535498, 41999720},{-76551570, 42000141},{-76622314, 42000485},{-76748524, 42001684},{-76815061, 42001671},{-76815383, 42001897},{-76835266, 42002134},{-76901558, 42001576},{-76902891, 42001872},{-76937206, 42001672},{-77020200, 42000469},{-77063676, 42000461},{-77126846, 41999414},{-77171024, 41999421},{-77198095, 41999793},{-77248266, 41999624},{-77505308, 42000070},{-77584737, 41999397},{-77653280, 41999445},{-77776710, 41998428},{-77817187, 41998562},{-77828396, 41998259},{-77840208, 41998503},{-77904659, 41998366},{-77997508, 41998758},{-78029743, 41999427},{-78124731, 42000451},{-78271204, 41998968},{-78344733, 41999606},{-78596650, 41999877},{-78749650, 41998110},{-78874759, 41997559},{-79000410, 41999125},{-79124768, 41999507},{-79138468, 41999258},{-79178570, 41999458},{-79249772, 41998807},{-79374772, 41998706},{-79472520, 41998254},{-79527172, 41998555},{-79552197, 41998384},{-79573243, 41998821},{-79624377, 41999064},{-79631281, 41998761},{-79645461, 41998859}});
    Geometry::Polygon shape(t);

    Graphics::Canvas canvas(600,600);

    for (int i = 1; i < 11; i++) {
        canvas.add_shape(shape, false, Graphics::Color(255, 50, 50), i);
        canvas.draw();
        canvas.clear();
    }
    
    // assert_equal("checking area function", area(shape), 0.5);
    // assert_equal("testing center coord 1", center(shape)[0], 0.333333);
    // assert_equal("testing center coord 2", center(shape)[1], 0.333333);
}