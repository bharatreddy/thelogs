class StockApiMashape(object):
    """
    More stock related data like listed and current prices etc.
    These are from mashape api collection, some functions here 
    are used as a backup others as primary source.
    """

    def __init__(self):
        # the mashape api key
        self.mashapeKey = "KutfyayVBRmsh2LTglXZgOFGYCcAp150IzAjsnsyuXvMiCwBER"

    def get_equity_list(self):
        import unirest
        # These code snippets use an open-source library. http://unirest.io/python
        equityListResponse = unirest.get("https://stockviz.p.mashape.com/marketdata/equitylist",
          headers={
            "X-Mashape-Key": self.mashapeKey
          }
        )
        print equityListResponse