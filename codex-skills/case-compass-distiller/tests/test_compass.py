import tempfile, unittest, sys, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import compass

class Tests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.p=Path(self.t.name)/'p'; compass.init_project(self.p,'t')
        self.src=self.p/'raw.txt'; self.src.write_text('甲：你来了？\n乙：我一直在。\n\n灯灭了。',encoding='utf-8')
        class A: pass
        a=A(); a.id='c1'; a.title='x'; a.status='success'; a.domain='writing'; a.job='screenplay'; a.format='script'; a.audience='general'; a.tone='克制'; a.constraints='双人'; a.starting_state=''; a.ending_state=''; a.why_successful='ok'; a.proof_type='test'; a.score=8.3
        c=compass.auto_case_from_source(self.src,a); compass.dump(self.p/'cases'/'c1.json',c)
        self.task={'id':'t1','title':'t','coordinates':{'domain':'writing','job':'screenplay','format':'script','audience':'general','length':30,'tone':['克制'],'constraints':['双人']},'input':'写一段','must_include':[],'must_avoid':[]}; compass.dump(self.p/'tasks'/'t1.json',self.task)
    def tearDown(self): self.t.cleanup()
    def test_fp(self):
        fp=compass.text_fingerprint('甲：好。\n乙：为什么？'); self.assertEqual(fp['speaker_count'],2)
    def test_case_valid(self): self.assertFalse(compass.validate_case(compass.load(self.p/'cases'/'c1.json')))
    def test_layer_score(self): self.assertGreater(compass.layer_score(compass.load(self.p/'cases'/'c1.json'),self.task,'voice'),.5)
    def test_map(self): self.assertEqual(compass.build_map(self.p)['case_count'],1)
    def test_route_layers(self): self.assertEqual(set(compass.route(self.p,self.p/'tasks'/'t1.json',1,True)['layer_leaders']),set(compass.LAYERS))
    def test_compile(self):
        out=self.p/'outputs'/'x.md'; compass.compile_prompt(self.p,self.p/'tasks'/'t1.json',out,1); self.assertIn('四层局部先例',out.read_text(encoding='utf-8'))
    def test_overlap(self): self.assertGreaterEqual(compass.shared_run_length('abcdefghijklmnop',['xxabcdefghijklmnopyy']),16)
    def test_audit(self):
        out=self.p/'outputs'/'o.txt'; out.write_text('甲：来了。\n乙：没有。',encoding='utf-8'); r=compass.audit_output(self.p,self.p/'tasks'/'t1.json',out); self.assertIn('mechanical_score_10',r)
    def test_validate(self): self.assertEqual(compass.validate_project(self.p),0)
if __name__=='__main__': unittest.main()
