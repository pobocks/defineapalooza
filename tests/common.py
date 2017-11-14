from vcr import VCR
import defineapalooza

app = defineapalooza.app.test_client()
betamax = VCR(record_mode="new_episodes", func_path_generator = lambda test: "tests/fixtures/cassettes/{}--{}.yaml".format(test.__module__, test.__name__))
