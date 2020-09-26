import customer
import supplier
import allocator
import verifier
import time


v = verifier.Verifier(tenant="sh4")
c = customer.Trader(tenant="sh1")
s1 = supplier.Trader(tenant="sh2", seed=2)
s2 = supplier.Trader(tenant="sh3", seed=3)
a = allocator.Allocator()

print(c.producer.last_sequence_id())
c.post_offer(oid=0, replicas=2)
s1.post_offer(oid=0)
s2.post_offer(oid=0)


time.sleep(10)
