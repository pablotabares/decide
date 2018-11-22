from rest_framework.views import APIView
from rest_framework.response import Response
import random


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weight(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weightedRandomSelection(self, options):
        print(options)
        out = []
        nVotes = 0
        for opt in options:
            nVotes += opt["votes"]
        randomValue = random.randint(0, nVotes-1)
        print("Random Value: " + str(randomValue))
        found = False
        for i in range(0, len(options)):
            randomValue -= options[i]["votes"]
            if randomValue < 0 and not found:
                out.append({
                    **options[i],
                    'postproc': 1
                })
                found = True
            else:
                out.append({
                    **options[i],
                    'postproc': 0
                })
        out.sort(key=lambda x: -x['postproc'])
        print(str(out))
        return Response(out)

    def hondt(self, options, escanyos):
        out = []
        votos = []
        reparto = []

        for opt in options:
            votos.append({
                'votes': opt['votes'],
            })
            reparto.append({
                'escanyos': 0
            })

        for i in range(escanyos):
            max = 0;
            imax = 0;
            for i in range(len(votos)):
                cociente = votos[i]['votes'] / (reparto[i]['escanyos'] + 1)
                if (cociente > max):
                    max = cociente
                    imax = i
            reparto[imax]['escanyos'] += 1
        for i in range(len(options)):
            out.append({
                **options[i],
                'postproc': reparto[i]['escanyos'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t =='WEIGHT':
            return self.weight(opts)
        elif t == 'WEIGHTED-RANDOM':
            return self.weightedRandomSelection(opts)
        elif t == 'HONDT':
            escanyos = request.data.get('escanyos', 1)
            return self.hondt(opts, escanyos)

        return Response({})
