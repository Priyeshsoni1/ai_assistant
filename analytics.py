class UsageAnalytics:
    def __init__(self):
        self.total_prompt_tokens=0
        self.total_completion_tokens=0
        self.total_cost=0
        self.total_requests=0
        self.total_latency=0

    def add_usage(self,prompt_tokens,completion_tokens,cost):
        self.total_prompt_tokens+=prompt_tokens
        self.total_completion_tokens+=completion_tokens
        self.total_cost+=cost
        self.total_requests+=1
    
    def get_stats(self):
        return {
            "request":self.total_requests,
            "prompt_tokens":self.total_prompt_tokens,
            "completion_tokens":self.total_completion_tokens,
            "total_tokens":self.total_completion_tokens+self.total_prompt_tokens,
            "cost":self.total_cost
        }
    def add_latency(self,latency):
        self.total_latency+=latency
    @property
    def average_latency(self):

        if self.total_requests == 0:
            return 0

        return (
            self.total_latency
            /
            self.total_requests
        )
