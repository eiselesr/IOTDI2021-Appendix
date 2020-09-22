reverse:
	docker-compose exec pulsar \
	bin/pulsar-admin functions create \
	--py /shared/reverse.py \
	--classname reverse \
	--inputs persistent://public/default/backwards \
	--output persistent://public/default/forwards \
	--tenant public \
	--namespace default \
	--name reverse

trigger:
	docker-compose exec pulsar \
	bin/pulsar-admin functions trigger \
	--name reverse \
	--tenant public \
	--namespace default \
	--trigger-value "sdrawrof won si tub sdrawkcab saw gnirts sihT"

trigger2:
	docker-compose exec pulsar \
	bin/pulsar-admin functions trigger \
	--name ReadInput \
	--tenant public \
	--namespace default \
	--trigger-value "sdrawrof won si tub sdrawkcab saw gnirts sihT"

delete:
	docker-compose exec pulsar \
	bin/pulsar-admin functions delete \
	--tenant public \
	--namespace default \
	--name ReadInput