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
        out = []
        nVotes = 0
        for opt in options:
            nVotes += opt["votes"]

        if nVotes == 0:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': False
                })
            return Response(out)

        randomValue = random.randint(0, nVotes-1)
        found = False
        for i in range(0, len(options)):
            randomValue -= options[i]["votes"]
            if randomValue < 0 and not found:
                out.append({
                    **options[i],
                    'postproc': True
                })
                found = True
            else:
                out.append({
                    **options[i],
                    'postproc': False
                })
        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def hondt(self, options, seats):
        out = []
        votes = []
        assignment = []

        for opt in options:
            votes.append({
                'votes': opt['votes'],
            })
            assignment.append({
                'seats': 0
            })

        for i in range(seats):
            max = 0;
            imax = 0;
            for i in range(len(votes)):
                cociente = votes[i]['votes'] / (assignment[i]['seats'] + 1)
                if (cociente > max):
                    max = cociente
                    imax = i
            assignment[imax]['seats'] += 1
        for i in range(len(options)):
            out.append({
                **options[i],
                'postproc': assignment[i]['seats'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def borda(self, options):
        option_positions = {} # {'A': [1,1,2], 'B':[2,2,1]}
        out = {} # {'A':'5', 'B':'4'}
        for opt in options:
            opcion = opt['option']
            posiciones = opt['positions']
            option_positions[opcion] = posiciones

        # We add 1, we have 2 options, I want to do 2+1 - posicion. Fist position 3-1=2 points
        nOptions = len(options) + 1
        for opt_p in option_positions:
            suma = 0
            for p in option_positions.get(opt_p): #We caugth positions [1,1,2]
                suma += nOptions - p #We add points
                
            out[opt_p] = suma 
        return Response(out)
 
    def multiquestion(self, questions):
        out = []

        for question in questions:
            votes = []

            for opt in question['options']:
                votes.append({
                    **opt,
                    'postproc': opt['votes'],
                })

            votes.sort(key=lambda x: -x['postproc'])
            out.append({
                'text': question['text'],
                'options': votes
            })
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | BORDA
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
            seats = request.data.get('seats', 1)
            return self.hondt(opts, seats)
        elif t == 'BORDA':
            return self.borda(opts)
            seats = request.data.get('seats', 1)
            return self.hondt(opts, seats)
        elif t == 'MULTIPLE':
            questions = request.data.get('questions', [])
            return self.multiquestion(questions)

        return Response({})
